document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded');
    window.player = new MusicPlayer();
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
        this.playlistBtn = document.getElementById('playlist-btn');
        this.playlistContainer = document.querySelector('.playlist-container');

        if (!this.hideButton || !this.musicPlayer || !this.playlistBtn || !this.playlistContainer) {
            console.error('Required elements not found:', {
                hideButton: !!this.hideButton,
                musicPlayer: !!this.musicPlayer,
                playlistBtn: !!this.playlistBtn,
                playlistContainer: !!this.playlistContainer
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
        this.audio.addEventListener('error', (e) => {
            console.error('Audio error:', e);
        });
        
        if (this.progress && this.progress.parentElement) {
            this.progress.parentElement.onclick = (e) => this.seek(e);
        }

        if (this.playlistBtn) {
            this.playlistBtn.onclick = (e) => {
                e.stopPropagation();
                this.togglePlaylist();
            };
        }

        document.addEventListener('click', (e) => {
            if (this.playlistContainer && 
                !this.playlistContainer.contains(e.target) && 
                !this.playlistBtn.contains(e.target)) {
                this.playlistContainer.classList.remove('show');
            }
        });

        document.addEventListener('keydown', (e) => {
            if (e.code === 'Space' && e.target === document.body) {
                e.preventDefault();
                this.togglePlay();
            }
        });
    }

    loadPlaylist(playlist) {
        if (!Array.isArray(playlist) || playlist.length === 0) {
            console.error('Invalid playlist format');
            return;
        }
        this.playlist = playlist;
        this.loadTrack(0);
        this.renderPlaylist();
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

            this.renderPlaylist();
        }
    }

    async loadLyrics(lrcUrl) {
        try {
            const response = await fetch(lrcUrl);
            if (!response.ok) throw new Error('Failed to load lyrics');
            const lrcText = await response.text();
            this.lyrics = this.parseLRC(lrcText);
            this.lastLyricIndex = -1;
        } catch (error) {
            console.error('加载歌词失败:', error);
            this.lyrics = {};
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
        if (Object.keys(this.lyrics).length === 0) return;

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
            const playPromise = this.audio.play();
            if (playPromise !== undefined) {
                playPromise.catch(error => {
                    console.error('播放失败:', error);
                });
            }
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
        this.audio.play().catch(error => {
            console.error('播放上一首失败:', error);
        });
        this.playBtn.querySelector('.play-icon').style.display = 'none';
        this.playBtn.querySelector('.pause-icon').style.display = 'block';
    }

    playNext() {
        let nextTrack = this.currentTrack + 1;
        if (nextTrack >= this.playlist.length) {
            nextTrack = 0;
        }
        this.loadTrack(nextTrack);
        this.audio.play().catch(error => {
            console.error('播放下一首失败:', error);
        });
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
            if (this.musicPlayer.classList.contains('player-hidden')) {
                this.playlistContainer.classList.remove('show');
            }
        }
    }

    togglePlaylist() {
        this.playlistContainer.classList.toggle('show');
        if (this.playlistContainer.classList.contains('show')) {
            this.renderPlaylist();
        }
    }

    renderPlaylist() {
        if (!this.playlistContainer) return;

        const content = this.playlistContainer.querySelector('.playlist-content');
        if (!content) return;

        content.innerHTML = this.playlist.map((track, index) => `
            <div class="playlist-item ${index === this.currentTrack ? 'playing' : ''}" 
                 onclick="player.playTrack(${index})">
                <div>
                    <div>${track.title}</div>
                    <div style="font-size: 0.8em; opacity: 0.7">${track.artist}</div>
                </div>
                ${index === this.currentTrack ? `
                    <div class="playing-indicator">
                        <span></span>
                        <span></span>
                        <span></span>
                    </div>
                ` : ''}
            </div>
        `).join('');
    }

    playTrack(index) {
        this.loadTrack(index);
        this.audio.play().catch(error => {
            console.error('播放选中歌曲失败:', error);
        });
        this.playBtn.querySelector('.play-icon').style.display = 'none';
        this.playBtn.querySelector('.pause-icon').style.display = 'block';
        this.renderPlaylist();
    }
} 