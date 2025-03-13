# playlist_generator.py
import os
import googleapiclient.discovery
from datetime import datetime
from dotenv import load_dotenv

# Configurações
load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")
SAVE_FOLDER = "playlists"

def search_videos(query, max_results=15):
    """Busca vídeos no YouTube e retorna lista de dicionários com dados"""
    youtube = googleapiclient.discovery.build(
        "youtube", "v3", developerKey=API_KEY
    )

    request = youtube.search().list(
        q=query,
        part="id,snippet",
        maxResults=max_results,
        type="video",
        order="relevance"  # relevance, date, rating, viewCount
    )
    
    response = request.execute()
    
    videos = []
    for item in response["items"]:
        video_id = item["id"]["videoId"]
        videos.append({
            "title": item["snippet"]["title"],
            "url": f"https://youtu.be/{video_id}",
            "channel": item["snippet"]["channelTitle"],
            "published": item["snippet"]["publishedAt"]
        })
    
    return videos

def save_playlist(query, videos):
    """Salva a playlist em um arquivo markdown"""
    if not os.path.exists(SAVE_FOLDER):
        os.makedirs(SAVE_FOLDER)
    
    filename = f"{datetime.now().strftime('%Y-%m-%d_%H-%M')}_{query[:20]}.md"
    filepath = os.path.join(SAVE_FOLDER, filename)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# Playlist: {query}\n\n")
        f.write(f"**Data de criação:** {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n")
        
        for idx, video in enumerate(videos, 1):
            f.write(f"{idx}. [{video['title']}]({video['url']})  \n")
            f.write(f"   *Canal: {video['channel']}*  \n")
            f.write(f"   Publicado em: {video['published'][:10]}  \n\n")
    
    print(f"Playlist salva em: {filepath}")
    return filepath

def main():
    query = input("Digite o tema da playlist: ").strip()
    
    print("\n🔍 Buscando vídeos...")
    try:
        videos = search_videos(query)
        if not videos:
            print("Nenhum vídeo encontrado!")
            return
            
        print("\n🎵 Vídeos encontrados:")
        for idx, video in enumerate(videos, 1):
            print(f"{idx}. {video['title']} ({video['url']})")
        
        filepath = save_playlist(query, videos)
        
        # Opcional: Abrir arquivo automaticamente
        if input("\nAbrir playlist? (s/n): ").lower() == "s":
            os.startfile(filepath)
            
    except Exception as e:
        print(f"Erro: {str(e)}")

if __name__ == "__main__":
    main()