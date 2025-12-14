"""VAD 智能音频分段模块 - 基于 silero-vad"""
import torch
import torchaudio
import logging

logger = logging.getLogger(__name__)

# 全局 VAD 模型（懒加载）
_vad_model = None
_vad_utils = None


def get_vad_model():
    """获取 VAD 模型（单例）"""
    global _vad_model, _vad_utils
    if _vad_model is None:
        _vad_model, _vad_utils = torch.hub.load(
            'snakers4/silero-vad', 'silero_vad', trust_repo=True
        )
    return _vad_model, _vad_utils


def detect_speech_segments(wav: torch.Tensor, sr: int = 16000) -> list:
    """检测语音段落
    
    Returns:
        list of (start_sample, end_sample) 语音区间
    """
    model, utils = get_vad_model()
    get_speech_timestamps = utils[0]
    
    # silero-vad 需要 16kHz 单声道
    if wav.dim() == 2:
        wav = wav[0]
    
    speech_timestamps = get_speech_timestamps(
        wav, model,
        sampling_rate=sr,
        threshold=0.5,
        min_speech_duration_ms=250,
        min_silence_duration_ms=300,
    )
    
    return [(s['start'], s['end']) for s in speech_timestamps]


def smart_segment(wav: torch.Tensor, sr: int = 16000, 
                  max_duration: float = 25.0, 
                  min_duration: float = 3.0) -> list:
    """智能分段：在静音处切分，确保每段 ≤ max_duration
    
    Args:
        wav: 音频张量 (1, samples) 或 (samples,)
        sr: 采样率
        max_duration: 最大段落时长（秒）
        min_duration: 最小段落时长（秒），过短则合并
    
    Returns:
        list of (start_sample, end_sample) 分段区间
    """
    if wav.dim() == 2:
        wav = wav[0]
    
    total_samples = wav.shape[0]
    max_samples = int(max_duration * sr)
    min_samples = int(min_duration * sr)
    
    # 检测语音段落
    speech_segments = detect_speech_segments(wav, sr)
    
    if not speech_segments:
        # 无语音，返回空
        return []
    
    # 合并语音段落，在静音处切分
    segments = []
    current_start = speech_segments[0][0]
    current_end = speech_segments[0][1]
    
    for i in range(1, len(speech_segments)):
        seg_start, seg_end = speech_segments[i]
        
        # 如果加上这段会超过 max_duration
        if seg_end - current_start > max_samples:
            # 当前段落够长，保存
            if current_end - current_start >= min_samples:
                segments.append((current_start, current_end))
            # 开始新段落
            current_start = seg_start
            current_end = seg_end
        else:
            # 继续累积
            current_end = seg_end
    
    # 保存最后一段
    if current_end - current_start >= min_samples:
        segments.append((current_start, current_end))
    elif segments:
        # 太短，合并到上一段（如果不超限）
        last_start, last_end = segments[-1]
        if current_end - last_start <= max_samples:
            segments[-1] = (last_start, current_end)
        else:
            segments.append((current_start, current_end))
    elif current_end > current_start:
        # 只有一小段，也保留
        segments.append((current_start, current_end))
    
    # 处理超长段落（连续说话无停顿的情况）
    final_segments = []
    for start, end in segments:
        duration = end - start
        if duration > max_samples:
            # 强制切分
            for chunk_start in range(start, end, max_samples):
                chunk_end = min(chunk_start + max_samples, end)
                if chunk_end - chunk_start >= min_samples:
                    final_segments.append((chunk_start, chunk_end))
        else:
            final_segments.append((start, end))
    
    logger.info(f"音频分段: 总时长 {total_samples/sr:.1f}s, 分成 {len(final_segments)} 段")
    return final_segments
