"""
Video Transcription Service
Sử dụng Gemini API để tự động tạo transcript từ video
Hỗ trợ: Upload file video, YouTube URL
"""
import os
import logging
import tempfile
import subprocess
import base64
from typing import Optional

import requests

logger = logging.getLogger(__name__)


class VideoTranscriber:
    """Service để tự động tạo transcript từ video bằng Gemini"""
    
    def __init__(self):
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        self.gemini_model = os.getenv('GEMINI_MODEL', 'gemini-2.0-flash')
    
    def transcribe_video(self, video_path: str = None, video_url: str = None) -> Optional[str]:
        """
        Tạo transcript từ video file hoặc YouTube URL
        
        Args:
            video_path: Đường dẫn file video local (upload)
            video_url: YouTube URL
            
        Returns:
            Transcript text hoặc None nếu lỗi
        """
        try:
            # Nếu là YouTube URL, lấy phụ đề có sẵn trước
            if video_url and ('youtube' in video_url.lower() or 'youtu.be' in video_url.lower()):
                # Ưu tiên 1: Lấy phụ đề có sẵn từ YouTube (nhanh, miễn phí)
                subtitle = self._get_youtube_subtitle(video_url)
                if subtitle:
                    logger.info("Got subtitle from YouTube")
                    return subtitle
                
                # Ưu tiên 2: Download video và dùng Gemini
                if self.gemini_api_key:
                    temp_video_path = self._download_youtube_video(video_url)
                    if temp_video_path:
                        transcript = self._call_gemini_video_api(temp_video_path)
                        try:
                            os.remove(temp_video_path)
                        except:
                            pass
                        if transcript:
                            return transcript
                
                # Ưu tiên 3: Fallback Gemini với URL
                if self.gemini_api_key:
                    return self._summarize_youtube_url(video_url)
                
                return None
            
            # Nếu là URL trực tiếp (không phải YouTube)
            elif video_url:
                if not self.gemini_api_key:
                    logger.warning("GEMINI_API_KEY not configured")
                    return None
                temp_video_path = self._download_direct_video(video_url)
                if temp_video_path:
                    transcript = self._call_gemini_video_api(temp_video_path)
                    try:
                        os.remove(temp_video_path)
                    except:
                        pass
                    return transcript
            
            # Nếu là file video upload
            elif video_path:
                if not self.gemini_api_key:
                    logger.warning("GEMINI_API_KEY not configured")
                    return None
                return self._call_gemini_video_api(video_path)
            
            logger.error("No video source provided")
            return None
            
        except Exception as e:
            logger.error(f"Error transcribing video: {e}")
            return None
    
    def _get_youtube_subtitle(self, youtube_url: str) -> Optional[str]:
        """Lấy phụ đề có sẵn từ YouTube (auto-generated hoặc manual)"""
        try:
            temp_dir = tempfile.mkdtemp()
            output_template = os.path.join(temp_dir, 'subtitle')
            
            # Lấy phụ đề tiếng Việt, nếu không có thì lấy auto-generated
            cmd = [
                'yt-dlp',
                '--skip-download',  # Không download video
                '--write-sub',      # Lấy phụ đề manual
                '--write-auto-sub', # Lấy phụ đề auto-generated
                '--sub-lang', 'vi,en',  # Ưu tiên tiếng Việt, sau đó English
                '--sub-format', 'vtt/srt/best',
                '--convert-subs', 'srt',
                '-o', output_template,
                '--no-playlist',
                youtube_url
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode != 0:
                logger.warning(f"yt-dlp subtitle error: {result.stderr}")
            
            # Tìm file phụ đề đã download
            subtitle_text = None
            for filename in os.listdir(temp_dir):
                if filename.endswith('.srt') or filename.endswith('.vtt'):
                    filepath = os.path.join(temp_dir, filename)
                    with open(filepath, 'r', encoding='utf-8') as f:
                        raw_subtitle = f.read()
                    # Parse và clean subtitle
                    subtitle_text = self._parse_subtitle(raw_subtitle)
                    break
            
            # Cleanup temp dir
            import shutil
            shutil.rmtree(temp_dir, ignore_errors=True)
            
            return subtitle_text
            
        except subprocess.TimeoutExpired:
            logger.error("YouTube subtitle download timeout")
            return None
        except Exception as e:
            logger.error(f"Error getting YouTube subtitle: {e}")
            return None
    
    def _parse_subtitle(self, raw_subtitle: str) -> str:
        """Parse file SRT/VTT thành text thuần"""
        import re
        
        lines = raw_subtitle.split('\n')
        text_lines = []
        
        for line in lines:
            line = line.strip()
            
            # Bỏ qua số thứ tự
            if line.isdigit():
                continue
            
            # Bỏ qua timestamp (00:00:00,000 --> 00:00:00,000)
            if re.match(r'^\d{2}:\d{2}:\d{2}[,\.]\d{3}\s*-->\s*\d{2}:\d{2}:\d{2}[,\.]\d{3}', line):
                continue
            
            # Bỏ qua header VTT
            if line.startswith('WEBVTT') or line.startswith('Kind:') or line.startswith('Language:'):
                continue
            
            # Bỏ qua các tag HTML/VTT
            line = re.sub(r'<[^>]+>', '', line)
            
            # Bỏ qua dòng trống
            if not line:
                continue
            
            # Tránh lặp lại dòng giống nhau liên tiếp
            if text_lines and line == text_lines[-1]:
                continue
            
            text_lines.append(line)
        
        return ' '.join(text_lines)
    
    def _download_youtube_video(self, youtube_url: str) -> Optional[str]:
        """Download video từ YouTube bằng yt-dlp"""
        try:
            temp_video = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False)
            temp_video_path = temp_video.name
            temp_video.close()
            
            # Sử dụng yt-dlp để download video
            cmd = [
                'yt-dlp',
                '-f', 'worst[ext=mp4]',  # Lấy chất lượng thấp nhất để giảm dung lượng
                '-o', temp_video_path,
                '--no-playlist',
                '--max-filesize', '20M',  # Giới hạn 20MB
                youtube_url
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode != 0:
                logger.error(f"yt-dlp error: {result.stderr}")
                return None
            
            if os.path.exists(temp_video_path) and os.path.getsize(temp_video_path) > 0:
                return temp_video_path
            
            return None
            
        except subprocess.TimeoutExpired:
            logger.error("YouTube download timeout")
            return None
        except Exception as e:
            logger.error(f"Error downloading YouTube video: {e}")
            return None
    
    def _download_direct_video(self, url: str) -> Optional[str]:
        """Download video từ URL trực tiếp"""
        try:
            temp_video = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False)
            
            response = requests.get(url, stream=True, timeout=60)
            response.raise_for_status()
            
            for chunk in response.iter_content(chunk_size=8192):
                temp_video.write(chunk)
            temp_video.close()
            
            if os.path.getsize(temp_video.name) > 0:
                return temp_video.name
            return None
            
        except Exception as e:
            logger.error(f"Error downloading direct URL: {e}")
            return None
    
    def _call_gemini_video_api(self, video_path: str) -> Optional[str]:
        """Gọi Gemini API để transcribe video"""
        try:
            # Đọc video file và encode base64
            with open(video_path, 'rb') as f:
                video_data = f.read()
            
            # Kiểm tra kích thước (Gemini giới hạn ~20MB cho inline data)
            if len(video_data) > 20 * 1024 * 1024:
                logger.warning("Video too large, extracting audio only")
                return self._transcribe_audio_only(video_path)
            
            video_base64 = base64.b64encode(video_data).decode('utf-8')
            
            # Xác định mime type
            ext = os.path.splitext(video_path)[1].lower()
            mime_types = {
                '.mp4': 'video/mp4',
                '.webm': 'video/webm',
                '.mov': 'video/quicktime',
                '.avi': 'video/x-msvideo',
            }
            mime_type = mime_types.get(ext, 'video/mp4')
            
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.gemini_model}:generateContent?key={self.gemini_api_key}"
            
            payload = {
                "contents": [{
                    "parts": [
                        {
                            "inline_data": {
                                "mime_type": mime_type,
                                "data": video_base64
                            }
                        },
                        {
                            "text": """Hãy xem video này và viết lại TOÀN BỘ nội dung lời nói trong video bằng tiếng Việt.

YÊU CẦU:
1. Viết lại chính xác những gì được nói trong video
2. Nếu có nhiều người nói, phân biệt họ
3. Bao gồm cả mô tả ngắn về những gì đang diễn ra trên màn hình (nếu liên quan đến bài học)
4. Viết theo dạng văn bản liền mạch, dễ đọc
5. Nếu video là bài giảng, ghi lại đầy đủ nội dung giảng dạy

Transcript:"""
                        }
                    ]
                }],
                "generationConfig": {
                    "temperature": 0.1,
                    "maxOutputTokens": 8000,
                }
            }
            
            response = requests.post(url, json=payload, timeout=120)
            
            if response.status_code == 200:
                data = response.json()
                candidates = data.get('candidates', [])
                if candidates:
                    text = candidates[0].get('content', {}).get('parts', [{}])[0].get('text', '')
                    return text.strip() if text else None
            else:
                logger.error(f"Gemini API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error calling Gemini API: {e}")
            return None
    
    def _transcribe_audio_only(self, video_path: str) -> Optional[str]:
        """Extract audio và transcribe nếu video quá lớn"""
        try:
            # Extract audio
            temp_audio = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False)
            temp_audio_path = temp_audio.name
            temp_audio.close()
            
            cmd = [
                'ffmpeg', '-i', video_path,
                '-vn',  # No video
                '-acodec', 'libmp3lame',
                '-ab', '64k',  # Low bitrate để giảm dung lượng
                '-y',
                temp_audio_path
            ]
            
            subprocess.run(cmd, capture_output=True, timeout=120)
            
            if not os.path.exists(temp_audio_path):
                return None
            
            # Đọc audio và gửi cho Gemini
            with open(temp_audio_path, 'rb') as f:
                audio_data = f.read()
            
            os.remove(temp_audio_path)
            
            audio_base64 = base64.b64encode(audio_data).decode('utf-8')
            
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.gemini_model}:generateContent?key={self.gemini_api_key}"
            
            payload = {
                "contents": [{
                    "parts": [
                        {
                            "inline_data": {
                                "mime_type": "audio/mpeg",
                                "data": audio_base64
                            }
                        },
                        {
                            "text": "Hãy viết lại TOÀN BỘ nội dung lời nói trong audio này bằng tiếng Việt. Viết chính xác, đầy đủ."
                        }
                    ]
                }],
                "generationConfig": {
                    "temperature": 0.1,
                    "maxOutputTokens": 8000,
                }
            }
            
            response = requests.post(url, json=payload, timeout=120)
            
            if response.status_code == 200:
                data = response.json()
                candidates = data.get('candidates', [])
                if candidates:
                    text = candidates[0].get('content', {}).get('parts', [{}])[0].get('text', '')
                    return text.strip() if text else None
            
            return None
            
        except Exception as e:
            logger.error(f"Error transcribing audio: {e}")
            return None
    
    def _summarize_youtube_url(self, youtube_url: str) -> Optional[str]:
        """Fallback: Yêu cầu Gemini tóm tắt từ YouTube URL (nếu download fail)"""
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.gemini_model}:generateContent?key={self.gemini_api_key}"
            
            payload = {
                "contents": [{
                    "parts": [{
                        "text": f"""Đây là link YouTube: {youtube_url}

Nếu bạn có thể truy cập video này, hãy:
1. Viết lại nội dung lời nói trong video
2. Mô tả những gì đang được dạy/trình bày
3. Tóm tắt các điểm chính

Nếu không truy cập được, hãy trả lời: "Không thể truy cập video. Vui lòng download video và upload lên hệ thống."
"""
                    }]
                }],
                "generationConfig": {
                    "temperature": 0.3,
                    "maxOutputTokens": 4000,
                }
            }
            
            response = requests.post(url, json=payload, timeout=60)
            
            if response.status_code == 200:
                data = response.json()
                candidates = data.get('candidates', [])
                if candidates:
                    text = candidates[0].get('content', {}).get('parts', [{}])[0].get('text', '')
                    if text and "Không thể truy cập" not in text:
                        return text.strip()
            
            return None
            
        except Exception as e:
            logger.error(f"Error summarizing YouTube URL: {e}")
            return None


# Singleton instance
video_transcriber = VideoTranscriber()
