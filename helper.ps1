Function get_demos {gci -Path "C:\Program Files (x86)\Steam\steamapps\common\Counter-Strike Global Offensive\game\csgo" -Filter *.dem -Recurse | % { "$($_.LastWriteTime) - $($_.FullName)" }}
function get_last_demo {gci "C:\Program Files (x86)\Steam\steamapps\common\Counter-Strike Global Offensive\game\csgo\replays\" -Filter *.dem | sort LastWriteTime | select -last 1 | % { set-clipboard -value $_.FullName }}
new-alias demos get_demos
new-alias lastdemo get_last_demo