---
title: Can I have 10ms Latency in Genshin Impact in Indonesia?
original-date: 2023-03-29T05:36:03+00:00
---

On the other day, my friend wonder if there will be an Indonesia ISP which allows him to play Genshin Impact with 10ms
ping.

Well, sorry to disappoint, but that's impossible. No, it's not because our technology is advanced enough (actually it
is), but it's not possible because there's hard limit related to the laws of physics: speed of light.

Why? First let's do some background. Genshin Impact is a single-player-oriented online game (weirdly). Since it's
online, it has various servers which are [Europe, America, Asia, Taiwan, and China](https://hoyo.global/game-servers/)
(only for people who live in China). Focus on the Asia, the server is hosted in Tokyo, Japan. My friend and I live in
Indonesia.

Now the reason why it's impossible because the distance between Indonesia and Japan is
[4821.39 km](https://distancecalculator.globefeed.com/Distance_Between_Countries_Result.asp?fromplace=Indonesia&toplace=Japan)
(Wolfram says it's 4912 km, see below). The speed of light constant is 299792458 m/s. Doing the calculation tells me
the minimum attainable latency by that distance is
[~16.38ms](https://www.wolframalpha.com/input?i=distance+from+Indonesia+to+Japan+divided+by+speed+of+light). That means
I need around 1 game frame at 60Hz monitor with VSync (or 1 game frame in Genshin Impact) to travel from Indonesia to
Japan. Multiply it by 2 for the round-trip latency gives you **~32.76ms**. By that alone, it's been concluded that
getting 10ms ping is **not possible**.

"_But data transfer instantly_"
No it's not. It still obey the laws of physics. That means in best case, your data transfer speed is limited by speed
of light. Well, the best case. In fact,
[light travels slower in fiber optics](https://www.jumpfiber.com/fiber-optics-speed-of-light-broadband-internet/),
around 2/3 of it. Taking that into account, the minimum attainable latency is **~49.15ms**. This can be worsen
furthermore by additional latency introduced by your WiFi and/or router and the ISP on both ends. That means, **49.15ms
is the data transfer speeds only, ignoring the router and ISP latency**.

"_Alright then, but I want exactly 10ms latency. I don't want to live in Japan though. Where should I live?_"
For this, I assume the overhead latency of your router and ISP is ignored (a.k.a exactly 0ms). For 10ms round-trip
latency, you need to live at 1998 km away from Tokyo, Japan. The closest would be South Korea, then Shanghai, China
(but in this case you better go with their China client with China servers for minimum latency), then area around
Sakhalin Oblast in Russia. If you want to take your router and ISP latency into account then you may want to live in
Yuzhno-Sakhalinsk in Russia or South Korea. It's as closest to Japan without having to live in Japan.

Note that if you have copper wire running from Russia to Japan instead of fiber optic, it
[may be faster](https://networkengineering.stackexchange.com/q/16438), but electromagnetic interference will assure ...

... you're gonna have a bad time

[Originally posted on cohost](https://web.archive.org/web/20250109214220/https://cohost.org/AuahDark/post/866048-can-i-have-10ms-late)
