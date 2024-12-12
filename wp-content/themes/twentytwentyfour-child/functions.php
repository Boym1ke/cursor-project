<?php
// 加载父主题样式
function twentytwentyfour_child_enqueue_styles() {
    wp_enqueue_style('twentytwentyfour-style', get_template_directory_uri() . '/style.css');
    wp_enqueue_style('twentytwentyfour-child-style',
        get_stylesheet_directory_uri() . '/style.css',
        array('twentytwentyfour-style')
    );
}
add_action('wp_enqueue_scripts', 'twentytwentyfour_child_enqueue_styles');

// 移除父主题的播放器资源加载函数
function remove_parent_player_assets() {
    remove_action('wp_enqueue_scripts', 'add_music_player_assets');
}
add_action('init', 'remove_parent_player_assets');

// 添加播放器相关脚本和样式
function child_music_player_assets() {
    $static_url = get_stylesheet_directory_uri() . '/static';
    
    // 添加播放器样式
    wp_enqueue_style(
        'music-player-style', 
        $static_url . '/style.css', 
        array(), 
        time(),
        'all'
    );
    
    // 添加播放器脚本
    wp_enqueue_script(
        'music-player-script',
        $static_url . '/player.js',
        array('jquery'),
        time(),
        true
    );
}
add_action('wp_enqueue_scripts', 'child_music_player_assets');

// 添加播放器HTML到页脚
function add_music_player_html() {
    $player_html_path = get_stylesheet_directory() . '/static/player.html';
    
    if (file_exists($player_html_path)) {
        include($player_html_path);
        ?>
        <script>
        jQuery(document).ready(function($) {
            try {
                const player = new MusicPlayer();
                
                const playlist = [
                    {
                        title: "Because You Loved Me",
                        artist: "Celine Dion",
                        url: "<?php echo get_stylesheet_directory_uri(); ?>/static/music/Celine-Dion-Because-You-Loved-Me.mp3",
                        cover: "<?php echo get_stylesheet_directory_uri(); ?>/static/images/bylm.jpg",
                        lrcUrl: "<?php echo get_stylesheet_directory_uri(); ?>/static/lyrics/because_you_loved_me.lrc",
                        volume: 1
                    },
                    {
                        title: "Imagine",
                        artist: "John Lennon",
                        url: "<?php echo get_stylesheet_directory_uri(); ?>/static/music/Imagine-John_Lennon.mp3",
                        cover: "<?php echo get_stylesheet_directory_uri(); ?>/static/images/imagine.jpg",
                        lrcUrl: "<?php echo get_stylesheet_directory_uri(); ?>/static/lyrics/Imagine-John_Lennon.lrc",
                        volume: 0.6
                    }
                ];
                
                player.loadPlaylist(playlist);
            } catch (error) {
                console.error('Player initialization error:', error);
            }
        });
        </script>
        <?php
    }
}
add_action('wp_footer', 'add_music_player_html', 999);

// 添加调试信息
function add_debug_info() {
    ?>
    <script>
    console.log('Theme paths:', {
        'Template directory': '<?php echo get_template_directory_uri(); ?>',
        'Stylesheet directory': '<?php echo get_stylesheet_directory_uri(); ?>',
        'Static folder exists': '<?php echo is_dir(get_stylesheet_directory() . "/static") ? "Yes" : "No"; ?>',
        'Player.js exists': '<?php echo file_exists(get_stylesheet_directory() . "/static/player.js") ? "Yes" : "No"; ?>',
        'Style.css exists': '<?php echo file_exists(get_stylesheet_directory() . "/static/style.css") ? "Yes" : "No"; ?>',
        'Player.html exists': '<?php echo file_exists(get_stylesheet_directory() . "/static/player.html") ? "Yes" : "No"; ?>'
    });
    </script>
    <?php
}
add_action('wp_footer', 'add_debug_info', 1);

// ��加欢迎动画
function add_welcome_animation() {
    if (is_front_page()) {
        ?>
        <div class="welcome-container">
            <img src="<?php echo get_stylesheet_directory_uri(); ?>/static/images/squirtle.gif" alt="Welcome" class="welcome-gif">
            <div class="falling-text-container">
                <?php
                $characters = array('欢','迎','来','到','我','的','网','站');
                foreach ($characters as $index => $char) {
                    echo "<span class='falling-character' style='animation-delay: {$index}s;'>{$char}</span>";
                }
                ?>
            </div>
        </div>
        <?php
    }
}
add_action('wp_body_open', 'add_welcome_animation');