import os
import logging
from pytubefix import YouTube, Playlist
from pytubefix.cli import on_progress
from moviepy.editor import AudioFileClip
import concurrent.futures
from tqdm import tqdm

# Suppress MoviePy logging
logging.getLogger("moviepy").setLevel(logging.WARNING)

def download_video_as_mp3(video_url, download_folder):
    video_title = ""
    try:
        # Download video
        video = YouTube(video_url, on_progress_callback=on_progress)
        video_title = video.title
        video_stream = video.streams.filter(only_audio=True).first()
        # downloaded_file = video_stream.download(output_path=download_folder)
        
        downloaded_file = f"{download_folder}/{video_title}.mp4"
        # Convert to MP3
        mp3_file = f"{download_folder}/{video_title}.mp3"
        
        audio_clip = AudioFileClip(downloaded_file)
        audio_clip.write_audiofile(mp3_file, logger=None)  # Disable MoviePy's logger
        audio_clip.close()

        # Remove the original file
        os.remove(downloaded_file)
        return True
    except OSError:
        print("couldn't find:", downloaded_file)
        return False

def download_videos_as_mp3(video_urls, download_folder):
    # Create download folder if it doesn't exist
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    with tqdm(total=len(video_urls), desc="Downloading videos") as pbar:
        with concurrent.futures.ProcessPoolExecutor() as executor:
            futures = {executor.submit(download_video_as_mp3, video_url, download_folder): video_url for video_url in video_urls}
            for future in concurrent.futures.as_completed(futures):
                success = future.result()
                pbar.update(1)  # Update progress bar regardless of success or failure


ABetterYouPodcast_videos = [
    "https://www.youtube.com/watch?v=dl41Wg0MuQw",
    "https://www.youtube.com/watch?v=Hc2zXmpyPig",
    "https://www.youtube.com/watch?v=7T1GftQSVPg",
    "https://www.youtube.com/watch?v=EGJeBlcJ5LI",
    "https://www.youtube.com/watch?v=85xKNVCvTGY",
    "https://www.youtube.com/watch?v=ZUnUnzVtD3Y",
    "https://www.youtube.com/watch?v=bFt1QpZLHh8",
    "https://www.youtube.com/watch?v=s1ldz9R0s20",
    "https://www.youtube.com/watch?v=-Lr1CRLPabo",
    "https://www.youtube.com/watch?v=TciOCPVWge0",
    "https://www.youtube.com/watch?v=NhUY-dLxO6I",
    "https://www.youtube.com/watch?v=kmpXz_-htuk",
    "https://www.youtube.com/watch?v=MclqPeV8RfY",
    "https://www.youtube.com/watch?v=joNAzJLBO1A",
    "https://www.youtube.com/watch?v=HR-IZwuRQx8",
    "https://www.youtube.com/watch?v=bslj87EFo_A",
    "https://www.youtube.com/watch?v=cIq2fCoBX64",
    "https://www.youtube.com/watch?v=hK6Sc2RXtPQ",
    "https://www.youtube.com/watch?v=N67IKBEq96k",
    "https://www.youtube.com/watch?v=Ppd1Ny9BG7A",
    "https://www.youtube.com/watch?v=IpYb0PpQwgQ",
    "https://www.youtube.com/watch?v=iy5LtM4zBpQ",
    "https://www.youtube.com/watch?v=bgQcNJqVESA",
    "https://www.youtube.com/watch?v=puruoNdguII",
    "https://www.youtube.com/watch?v=pS0qHvYoygY",
    "https://www.youtube.com/watch?v=ZYDf_hD3PBM",
    "https://www.youtube.com/watch?v=Nw8QF229UKU",
    "https://www.youtube.com/watch?v=b13sM4uTenE",
    "https://www.youtube.com/watch?v=2r-1he0rTV8",
    "https://www.youtube.com/watch?v=zywQo4amnKw",
    "https://www.youtube.com/watch?v=bgZ0XsdSidw",
    "https://www.youtube.com/watch?v=ATL8JWcuRUo",
    "https://www.youtube.com/watch?v=70dnECojCI4",
    "https://www.youtube.com/watch?v=dSBI5q9EVZY",
    "https://www.youtube.com/watch?v=beFU34Fpa-k",
    "https://www.youtube.com/watch?v=6AYcqth0J80",
    "https://www.youtube.com/watch?v=sXkp18aHPvo",
    "https://www.youtube.com/watch?v=cy8PCAtg8gM",
    "https://www.youtube.com/watch?v=yf2Xrlm1b_c",
    "https://www.youtube.com/watch?v=SlgKIJaoXd8",
    "https://www.youtube.com/watch?v=86YuktFrFF8",
    "https://www.youtube.com/watch?v=NTuO7O28COY",
    "https://www.youtube.com/watch?v=aOqN-bukU70",
    "https://www.youtube.com/watch?v=RJ9qmEhfeHo",
    "https://www.youtube.com/watch?v=H0dZj6qmtuY",
    "https://www.youtube.com/watch?v=MfvGRPJWWzw",
    "https://www.youtube.com/watch?v=mx7W65tASKs",
    "https://www.youtube.com/watch?v=WV0EIx7jriI",
    "https://www.youtube.com/watch?v=RzvbihnRo7A",
    "https://www.youtube.com/watch?v=jC3dA7-Vd5U"
]


SoloFlightPodcast_Videos = [
    "https://www.youtube.com/watch?v=O7Oin0qH28A",
    "https://www.youtube.com/watch?v=9bg3oOIStgM",
    "https://www.youtube.com/watch?v=VFv6-qmSDjI",
    "https://www.youtube.com/watch?v=Yl4ZMqwszVI",
    "https://www.youtube.com/watch?v=ROd4tcIW4_k",
    "https://www.youtube.com/watch?v=sFTH3UidMw4",
    "https://www.youtube.com/watch?v=af5wtwyWtOs",
    "https://www.youtube.com/watch?v=4tS0HT39Zb8",
    "https://www.youtube.com/watch?v=2-aYc-D2N6k",
    
]


Blue1Brown_Videos = [
    'https://www.youtube.com/watch?v=9-Jl0dxWQs8', 
    'https://www.youtube.com/watch?v=W3I3kAg2J7w', 
    'https://www.youtube.com/watch?v=eMlx5fFNoYc', 
    'https://www.youtube.com/watch?v=wjZofJX0v4M', 
    'https://www.youtube.com/watch?v=Cz4Q4QOuoo8', 
    'https://www.youtube.com/watch?v=KTzGBJPuJwM', 
    'https://www.youtube.com/watch?v=6a1fLEToyvU', 
    'https://www.youtube.com/watch?v=aXRTczANuIs', 
    'https://www.youtube.com/watch?v=QCX62YJCmGk', 
    'https://www.youtube.com/watch?v=d_qvLDhkg00', 
    'https://www.youtube.com/watch?v=YtkIWDE36qU', 
    'https://www.youtube.com/watch?v=NOCsdhzo6Jg', 
    'https://www.youtube.com/watch?v=IaSGqQa5O-M', 
    'https://www.youtube.com/watch?v=cy8r7WSuT1I', 
    'https://www.youtube.com/watch?v=zeJD6dqJ5lo', 
    'https://www.youtube.com/watch?v=KuXjwB4LzSA', 
    'https://www.youtube.com/watch?v=851U557j6HE', 
    'https://www.youtube.com/watch?v=cDofhN-RJqg', 
    'https://www.youtube.com/watch?v=VYQVlVoWoPY', 
    'https://www.youtube.com/watch?v=bOXCLR3Wric', 
    'https://www.youtube.com/watch?v=fRed0Xmc2Wg', 
    'https://www.youtube.com/watch?v=v68zYyaEmEA', 
    'https://www.youtube.com/watch?v=ltLUadnCyi0', 
    'https://www.youtube.com/watch?v=F3Qixy-r_rQ', 
    'https://www.youtube.com/watch?v=LqbZpur38nw', 
    'https://www.youtube.com/watch?v=-RdOwhmqP5s', 
    'https://www.youtube.com/watch?v=ojjzXyQCzso', 
    'https://www.youtube.com/watch?v=e50Bj7jn9IQ', 
    'https://www.youtube.com/watch?v=O85OWBJ2ayo', 
    'https://www.youtube.com/watch?v=lG4VkPoG3ko', 
    'https://www.youtube.com/watch?v=b3NxrZOu_CE', 
    'https://www.youtube.com/watch?v=X8jsijhllIA', 
    'https://www.youtube.com/watch?v=mH0oCDa74tE', 
    'https://www.youtube.com/watch?v=wTJI_WuZSwE', 
    'https://www.youtube.com/watch?v=D__UaR5MQao', 
    'https://www.youtube.com/watch?v=ppWPuXsnf1Q', 
    'https://www.youtube.com/watch?v=ZA4JkHKZM50', 
    'https://www.youtube.com/watch?v=gxAaO2rsdIs', 
    'https://www.youtube.com/watch?v=8idr1WZ1A7Q', 
    'https://www.youtube.com/watch?v=Kas0tIxDvrg', 
    'https://www.youtube.com/watch?v=U_85TaXbeIo', 
    'https://www.youtube.com/watch?v=HZGCoVF3YvM', 
    'https://www.youtube.com/watch?v=Agbh95KyWxY', 
    'https://www.youtube.com/watch?v=EK32jo7i5LQ', 
    'https://www.youtube.com/watch?v=M64HUIJFTZM', 
    'https://www.youtube.com/watch?v=v0YEaeIClKY', 
    'https://www.youtube.com/watch?v=-qgreAUpPwM', 
    'https://www.youtube.com/watch?v=r6sGWTCMz2k', 
    'https://www.youtube.com/watch?v=ToIXSwZ1pJU', 
    'https://www.youtube.com/watch?v=ly4S0oi3Yz8', 
    'https://www.youtube.com/watch?v=p_di4Zn4wz4', 
    'https://www.youtube.com/watch?v=jBsC34PxzoM', 
    'https://www.youtube.com/watch?v=brU5yLm9DZM', 
    'https://www.youtube.com/watch?v=jsYwFizhncE', 
    'https://www.youtube.com/watch?v=HEfHFsfGXjs', 
    'https://www.youtube.com/watch?v=GNcFjFmqEc8', 
    'https://www.youtube.com/watch?v=yuVqxCSsE7c', 
    'https://www.youtube.com/watch?v=_UoTTq651dE', 
    'https://www.youtube.com/watch?v=zjMuIxRvygQ', 
    'https://www.youtube.com/watch?v=d4EgbgTm0Bg', 
    'https://www.youtube.com/watch?v=Qe6o9j4IjTo', 
    'https://www.youtube.com/watch?v=pQa_tWZmlGs', 
    'https://www.youtube.com/watch?v=VcgJro0sTiM', 
    'https://www.youtube.com/watch?v=rB83DpBJQsE', 
    'https://www.youtube.com/watch?v=CfW845LNObM', 
    'https://www.youtube.com/watch?v=8GPy_UMV-08', 
    'https://www.youtube.com/watch?v=b7FxPsqfkOY', 
    'https://www.youtube.com/watch?v=bcPTiiiYDs8', 
    'https://www.youtube.com/watch?v=d-o3eB9sfls', 
    'https://www.youtube.com/watch?v=MBnnXbOM5S4', 
    'https://www.youtube.com/watch?v=spUNpyF58BY', 
    'https://www.youtube.com/watch?v=VvCytJvd4H0', 
    'https://www.youtube.com/watch?v=liL66CApESk', 
    'https://www.youtube.com/watch?v=OkmNXy7er84', 
    'https://www.youtube.com/watch?v=tIeHLnjs5U8', 
    'https://www.youtube.com/watch?v=Ilg3gGewQ5U', 
    'https://www.youtube.com/watch?v=IHZwWFHWa-w', 
    'https://www.youtube.com/watch?v=aircAruvnKk', 
    'https://www.youtube.com/watch?v=MzRCDLre1b4', 
    'https://www.youtube.com/watch?v=zwAD6dRSVyI', 
    'https://www.youtube.com/watch?v=3s7h2MHQtxc', 
    'https://www.youtube.com/watch?v=S9JGmA5_unY', 
    'https://www.youtube.com/watch?v=bBC-nXj3Ng4', 
    'https://www.youtube.com/watch?v=QJYmyhnaaek', 
    'https://www.youtube.com/watch?v=NaL_Cb42WyY', 
    'https://www.youtube.com/watch?v=3d6DsjIBzJ4', 
    'https://www.youtube.com/watch?v=BLkz5LGWihw', 
    'https://www.youtube.com/watch?v=FnJqaIESC2s', 
    'https://www.youtube.com/watch?v=rfG8ce4nNh0', 
    'https://www.youtube.com/watch?v=kfF40MiS7zA', 
    'https://www.youtube.com/watch?v=qb40J4N1fa4', 
    'https://www.youtube.com/watch?v=m2MIpDrF7Es', 
    'https://www.youtube.com/watch?v=YG15m2VwSjA', 
    'https://www.youtube.com/watch?v=S0_qX4VJhMQ', 
    'https://www.youtube.com/watch?v=9vKqVkMQHKk', 
    'https://www.youtube.com/watch?v=WUvTyaaNkzM', 
    'https://www.youtube.com/watch?v=mvmuCPvRoWQ', 
    'https://www.youtube.com/watch?v=gB9n2gHsHN4', 
    'https://www.youtube.com/watch?v=IxNb1WG_Ido', 
    'https://www.youtube.com/watch?v=sD0NjbwqlYw', 
    'https://www.youtube.com/watch?v=bdMfjfT0lKk', 
    'https://www.youtube.com/watch?v=2SUvWfNJSsM', 
    'https://www.youtube.com/watch?v=R7p-nPg8t_g', 
    'https://www.youtube.com/watch?v=AmgkSdhK4K8', 
    'https://www.youtube.com/watch?v=TgKwz5Ikpc8', 
    'https://www.youtube.com/watch?v=PFDu9oVAE-g', 
    'https://www.youtube.com/watch?v=P2LTAUO1TdA', 
    'https://www.youtube.com/watch?v=eu6i7WJeinw', 
    'https://www.youtube.com/watch?v=BaM7OCEm3G0', 
    'https://www.youtube.com/watch?v=LyGKycYT2v0', 
    'https://www.youtube.com/watch?v=v8VSDg_WQlA', 
    'https://www.youtube.com/watch?v=uQhTuRlWMxw', 
    'https://www.youtube.com/watch?v=Ip3X9LOh2dk', 
    'https://www.youtube.com/watch?v=rHLEWRxRGiM', 
    'https://www.youtube.com/watch?v=XkY2DOUCWMU', 
    'https://www.youtube.com/watch?v=kYB8IZa5AuE', 
    'https://www.youtube.com/watch?v=k7RM-ot2NWY', 
    'https://www.youtube.com/watch?v=fNk_zzaMoSs', 
    'https://www.youtube.com/watch?v=kjBOesZCoqc', 
    'https://www.youtube.com/watch?v=sULa9Lc4pck', 
    'https://www.youtube.com/watch?v=Iq1a_KJTWJ8', 
    'https://www.youtube.com/watch?v=Cld0p3a43fU', 
    'https://www.youtube.com/watch?v=RU0wScIj36o', 
    'https://www.youtube.com/watch?v=cyW5z-M2yzw', 
    'https://www.youtube.com/watch?v=1SMmc9gQmHQ', 
    'https://www.youtube.com/watch?v=XFDM1ip5HdU', 
    'https://www.youtube.com/watch?v=-9OUyo8NFZg', 
    'https://www.youtube.com/watch?v=zLzLxVeqdQg', 
    'https://www.youtube.com/watch?v=F_0yfvm0UoU'
]

JustAlexPodcast_Videos = [
    "https://www.youtube.com/watch?v=TQhXclq9KY4",
    "https://www.youtube.com/watch?v=PAhAjb2HoJ4",
    "https://www.youtube.com/watch?v=Y5Jm3WZYNNE",
    "https://www.youtube.com/watch?v=9bX2NKs3gkk",
    
]

# vids = ["https://www.youtube.com/watch?v=klRb0_BAX9g"]

allVideos = [ABetterYouPodcast_videos, SoloFlightPodcast_Videos, Blue1Brown_Videos, JustAlexPodcast_Videos]
folderNames = ["A Better You Podcast", "Solo Flight Podcast", "3Blue1Brown", "Just Alex Podcast"]

if __name__ == '__main__':
    for folder, videos in zip(folderNames, allVideos):
    
        # Specify the folder to save the MP3 files
        download_folder = f'Dataset/Raw/{folder}'

        download_videos_as_mp3(videos, download_folder)