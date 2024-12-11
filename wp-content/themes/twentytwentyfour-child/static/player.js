document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded');
    const player = new MusicPlayer();
});

class MusicPlayer {
    constructor() {
        this.audio = new Audio();
        this.playlist = [];
        this.currentTrack = 0;
        this.lyrics = {};
        this.lastLyricIndex = -1;
        
        this.initializePlayer();
        this.bindEvents();
    }

    initializePlayer() {
        this.playBtn = document.getElementById('play-btn');
        this.prevBtn = document.getElementById('prev-btn');
        this.nextBtn = document.getElementById('next-btn');
        this.progress = document.getElementById('progress');
        this.currentTimeSpan = document.getElementById('current-time');
        this.durationSpan = document.getElementById('duration');
        this.hideButton = document.getElementById('hide-player');
        this.musicPlayer = document.getElementById('floating-player');

        if (!this.hideButton || !this.musicPlayer) {
            console.error('Required elements not found:', {
                hideButton: !!this.hideButton,
                musicPlayer: !!this.musicPlayer
            });
        }
    }

    bindEvents() {
        if (this.hideButton && this.musicPlayer) {
            this.hideButton.onclick = (e) => {
                e.stopPropagation();
                this.toggleHide();
            };

            this.musicPlayer.onclick = (e) => {
                if (this.musicPlayer.classList.contains('player-hidden')) {
                    this.toggleHide();
                }
            };
        }

        this.playBtn.onclick = () => this.togglePlay();
        this.prevBtn.onclick = () => this.playPrevious();
        this.nextBtn.onclick = () => this.playNext();
        
        this.audio.addEventListener('timeupdate', () => this.updateProgress());
        this.audio.addEventListener('ended', () => this.playNext());
        
        if (this.progress && this.progress.parentElement) {
            this.progress.parentElement.onclick = (e) => this.seek(e);
        }
    }

    loadPlaylist(playlist) {
        this.playlist = playlist;
        this.loadTrack(0);
    }

    loadTrack(index) {
        if (index >= 0 && index < this.playlist.length) {
            this.currentTrack = index;
            const track = this.playlist[index];
            
            this.audio.src = track.url;
            this.audio.volume = track.volume || 1.0;
            
            document.getElementById('song-title').textContent = track.title;
            document.getElementById('artist-name').textContent = track.artist;
            document.getElementById('cover-art').src = track.cover;
            
            if (track.lrcUrl) {
                this.loadLyrics(track.lrcUrl);
            }
        }
    }

    async loadLyrics(lrcUrl) {
        try {
            const response = await fetch(lrcUrl);
            const lrcText = await response.text();
            this.lyrics = this.parseLRC(lrcText);
            this.lastLyricIndex = -1;
        } catch (error) {
            console.error('加载歌词失败:', error);
        }
    }

    parseLRC(lrc) {
        const lines = lrc.split('\n');
        const lyrics = {};
        
        lines.forEach(line => {
            const match = line.match(/\[(\d{2}):(\d{2})\.(\d{2,3})\](.*)/);
            if (match) {
                const minutes = parseInt(match[1]);
                const seconds = parseInt(match[2]);
                const time = minutes * 60 + seconds;
                lyrics[time] = match[4].trim();
            }
        });
        
        return lyrics;
    }

    updateLyrics() {
        const currentTime = Math.floor(this.audio.currentTime);
        const times = Object.keys(this.lyrics).map(Number).sort((a, b) => a - b);
        
        const currentIndex = times.findIndex(time => time > currentTime);
        const currentLyricTime = times[currentIndex - 1];
        
        if (currentIndex - 1 !== this.lastLyricIndex && currentLyricTime !== undefined) {
            this.lastLyricIndex = currentIndex - 1;
            
            const container = document.querySelector('.lyrics-container');
            const wrapper = container.querySelector('.lyrics-wrapper');
            
            wrapper.innerHTML = '';
            
            for (let i = -1; i <= 1; i++) {
                const index = currentIndex + i - 1;
                const div = document.createElement('div');
                div.className = `lyrics-line ${i === 0 ? 'lyrics-current' : ''}`;
                
                if (index >= 0 && index < times.length) {
                    div.textContent = this.lyrics[times[index]];
                } else {
                    div.textContent = ' ';
                }
                
                wrapper.appendChild(div);
            }
        }
    }

    togglePlay() {
        if (this.audio.paused) {
            this.audio.play();
            this.playBtn.querySelector('.play-icon').style.display = 'none';
            this.playBtn.querySelector('.pause-icon').style.display = 'block';
        } else {
            this.audio.pause();
            this.playBtn.querySelector('.play-icon').style.display = 'block';
            this.playBtn.querySelector('.pause-icon').style.display = 'none';
        }
    }

    playPrevious() {
        let prevTrack = this.currentTrack - 1;
        if (prevTrack < 0) {
            prevTrack = this.playlist.length - 1;
        }
        this.loadTrack(prevTrack);
        this.audio.play();
        this.playBtn.querySelector('.play-icon').style.display = 'none';
        this.playBtn.querySelector('.pause-icon').style.display = 'block';
    }

    playNext() {
        let nextTrack = this.currentTrack + 1;
        if (nextTrack >= this.playlist.length) {
            nextTrack = 0;
        }
        this.loadTrack(nextTrack);
        this.audio.play();
        this.playBtn.querySelector('.play-icon').style.display = 'none';
        this.playBtn.querySelector('.pause-icon').style.display = 'block';
    }

    updateProgress() {
        const duration = this.audio.duration;
        const currentTime = this.audio.currentTime;
        
        if (duration) {
            const progressPercent = (currentTime / duration) * 100;
            this.progress.style.width = `${progressPercent}%`;
            
            this.currentTimeSpan.textContent = this.formatTime(currentTime);
            this.durationSpan.textContent = this.formatTime(duration);
            
            this.updateLyrics();
        }
    }

    seek(e) {
        const progressBar = this.progress.parentElement;
        const percent = e.offsetX / progressBar.offsetWidth;
        this.audio.currentTime = percent * this.audio.duration;
    }

    formatTime(seconds) {
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = Math.floor(seconds % 60);
        return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
    }

    toggleHide() {
        if (this.musicPlayer) {
            this.musicPlayer.classList.toggle('player-hidden');
            console.log('Toggle hide state:', this.musicPlayer.classList.contains('player-hidden'));
        }
    }
} 