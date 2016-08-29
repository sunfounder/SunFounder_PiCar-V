pid=`ps -A | grep mjpg_streamer | grep -v "grep" | head -n 1`
echo \'$pid\'
sudo kill $pid
