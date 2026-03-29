---
title: "SIF Note Handling: Observation & Accuracy."
original-date: 2018-05-01T14:04:00+08:00
---
Recently some people complain about Live Simulator: 2 timing. I exactly remember that Live Simulator: 2 code the note
accuracy based on my [previous article](sif1-note-handling.html) regarding SIF note handling, but they say it doesn't
seems right, so I decide to test it in Live Simulator: 2 and SIF. The difference were significant but not very. I
decide to record my SIF note tapping observation video below.

<iframe width="560" height="315" src="https://www.youtube-nocookie.com/embed/-0zvBJela3c?si=29pMnWHEpjxqwhrC" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
(If the YouTube embed doesn't appear, open it in new tab: <https://www.youtube.com/watch?v=-0zvBJela3c>)

Sorry for the 30 FPS video. Google Play Games just can't record thing in 60 FPS at that time. I used 1.6 second note
speed (note velocity = 250px/s) and [WHITE FIRST LOVE] (Normal) beatmap.

As you may know, SIF use this timing table:

| Judgement   | Init. Accuracy Val. (px) | Acc. Dist. from Icon (px) |
| ----------- | ------------------------ | ------------------------- |
| **PERFECT** | 16                       | 12.8                      |
| **GREAT**   | 40                       | 32                        |
| **GOOD**    | 64                       | 51.2                      |
| **BAD**     | 112                      | 89.6                      |
| **MISS**    | 128                      | 102.4                     |
(For more information, see the original image here: <../assets/sif_judgement_value.png>)

From now on, ignore the "Accuracy Distance" column and focus on "Judgement" and "Initial Accuracy" column. However the
statement "For swing, Perfect = Great accuracy; Great = Good accuracy" still applies in this context.

Probably you were wondering, how big is 128 pixel? The short answer is, the tap icon diameter. Tap icon diameter is
roughly 128 pixels (there are some padding added but actual size in-game files is 128x128px).

One example, when I tap the 2nd note in that video, I time it to be slightly inside idol icon radius and getting good.
It's actually true, because the tap icon diameter is 128px, and as basic geometry math tells you that circle radius is
half of the diameter, so the tap icon radius is 64 pixels. If you look at the table, 40-64 pixel result in "Good"
judgement.

Another example for long note case, when I started the long note in 3rd note, but when I release it, it result in miss.
It may looks like should fall in "Bad" range (because the distance is <128px) but if you look it correctly in table
above, 112-128 range result in "Miss" judgement.

Now what's the use of that "128px" in Miss row? That 128 value is only used for tapping the note, not for release.
Look at 0:37 and you'll see long note which I tap and result in "Bad" judgement (and if you observe carefully, the
distance is actually 128px). But why? The answer is, to prevent you tapping the note too early. Say, you tap the note
in 200px distance, but since maximum distance is 128px, the game doesn't register "tap" to the note.

What if you missed the note completely? In 0:54, I missed a note in the left side, but it's count as "Miss" when the
distance of the note is 128px. In this case, we can conclude that distance 112px or higher result in "Bad" for single
note and result in "Miss" for long note trail.

That observation **assume** 0 timing offset. If timing offset start into play, things start get trickier. I haven't
observe when timing offset comes into play, so the rest of this writing is entirely subjective. Winshley said from
reddit that "it's almost impossible to get late "Bad" tap with -50 timing offset". That means the note judgement tap
range is shifted, but not the 128px range. If my calculation is right, the late "Bad" tap (64-112px range) in -50
timing offset, is 114-162px. However, the maximum limit is 128px, so the range is actually 114-128px. There's only 14px
gap between, and with note speed of 0.5 second (to be exact, 0.571428 second), it will be impossible to get late "Bad"
tap at all and you'll either get late "Good" or late "Miss".

Because this is based on observation, real-life observation, that means my previous article is invalid (which is
completely theoretical). I'll plan to fix all of this mess in Live Simulator: 2 and add SIF timing offset instead of
global offset which shifts the whole beatmap time.

At last, I've played [WHITE FIRST LOVE] song in 5 days a row and I'm not even getting bored of it.

[WHITE FIRST LOVE]: https://www.youtube.com/watch?v=uFG5GQnfJyI
