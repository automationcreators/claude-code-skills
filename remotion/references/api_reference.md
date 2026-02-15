# Remotion API Reference

Complete API cheat sheet for Remotion v4. Consult this when you need exact function signatures, prop types, or package imports.

## Hooks

### useCurrentFrame()

```tsx
import { useCurrentFrame } from "remotion";

const frame = useCurrentFrame();
// Returns: number (0-indexed frame within current Sequence/Composition)
```

Inside a `<Sequence from={30}>`, `useCurrentFrame()` returns 0 when the global frame is 30.

### useVideoConfig()

```tsx
import { useVideoConfig } from "remotion";

const { fps, durationInFrames, width, height, id, defaultProps } = useVideoConfig();
// fps: number — frames per second
// durationInFrames: number — total frames in current composition
// width: number — composition width in pixels
// height: number — composition height in pixels
// id: string — composition ID
// defaultProps: object — default props of the composition
```

### useCurrentScale()

```tsx
import { useCurrentScale } from "remotion";

const scale = useCurrentScale();
// Returns: number — the factor by which the video is scaled down in the Studio/Player
// Useful for rendering high-DPI text or adapting stroke widths
```

### getRemotionEnvironment()

```tsx
import { getRemotionEnvironment } from "remotion";

const env = getRemotionEnvironment();
// env.isStudio — true in Remotion Studio
// env.isRendering — true during npx remotion render
// env.isPlayer — true in @remotion/player
```

## Animation Functions

### interpolate()

```tsx
import { interpolate } from "remotion";

const value = interpolate(
  input,       // number — typically useCurrentFrame()
  inputRange,  // [number, number, ...] — must be monotonically increasing
  outputRange, // [number, number, ...] — same length as inputRange
  options?     // InterpolateOptions (see below)
);

// Options:
interface InterpolateOptions {
  easing?: (t: number) => number;        // Default: Easing.linear
  extrapolateLeft?: "extend" | "clamp" | "identity";   // Default: "extend"
  extrapolateRight?: "extend" | "clamp" | "identity";  // Default: "extend"
}
```

**Multi-step interpolation:**

```tsx
const opacity = interpolate(frame, [0, 20, 40, 60], [0, 1, 1, 0], {
  extrapolateLeft: "clamp",
  extrapolateRight: "clamp",
});
// 0→20: fade in, 20→40: hold at 1, 40→60: fade out
```

### interpolateColors()

```tsx
import { interpolateColors } from "remotion";

const color = interpolateColors(
  input,       // number
  inputRange,  // number[]
  colorRange   // string[] — hex, rgb(), rgba(), hsl(), named colors
);

// Example:
const bgColor = interpolateColors(frame, [0, 60], ["#ff0000", "#0000ff"]);
```

### spring()

```tsx
import { spring } from "remotion";

const value = spring({
  frame,             // number — useCurrentFrame()
  fps,               // number — useVideoConfig().fps
  config?: {
    damping?: number,    // Default: 10 — higher = less bounce
    mass?: number,       // Default: 1 — higher = slower
    stiffness?: number,  // Default: 100 — higher = snappier
    overshootClamping?: boolean, // Default: false — clamp to target
  },
  from?: number,     // Default: 0 — start value
  to?: number,       // Default: 1 — end value
  durationInFrames?: number, // Optional — cap spring duration
  durationRestThreshold?: number, // Default: 0.005
  delay?: number,    // Default: 0 — delay in frames before start
  reverse?: boolean, // Default: false — play spring backwards
});
```

**Common spring configs:**

| Style | damping | mass | stiffness |
|-------|---------|------|-----------|
| Snappy | 15 | 0.5 | 200 |
| Bouncy | 8 | 1 | 150 |
| Gentle | 20 | 1 | 80 |
| Heavy | 12 | 2 | 100 |
| Instant | 30 | 0.5 | 300 |

### measureSpring()

```tsx
import { measureSpring } from "remotion";

const durationInFrames = measureSpring({
  fps: 30,
  config: { damping: 12, stiffness: 200, mass: 0.5 },
  threshold?: 0.005, // Default: 0.005 — when spring is "done"
});
// Returns: number — frames until spring settles (useful for Sequence durations)
```

### Easing

```tsx
import { Easing } from "remotion";

Easing.linear        // (t) => t
Easing.ease          // Default CSS ease
Easing.quad          // (t) => t * t
Easing.cubic         // (t) => t * t * t
Easing.sin           // Sine-based
Easing.circle        // Circular
Easing.exp           // Exponential
Easing.elastic(1)    // Elastic with bounciness
Easing.back(1.5)     // Overshoot
Easing.bounce        // Bounce at end
Easing.bezier(x1, y1, x2, y2)  // Custom bezier curve

// Modifiers — wrap any easing:
Easing.in(Easing.cubic)      // Slow start
Easing.out(Easing.cubic)     // Slow end
Easing.inOut(Easing.cubic)   // Slow start and end
```

## Layout Components

### `<Composition>`

Registers a video in Root.tsx:

```tsx
import { Composition } from "remotion";

<Composition
  id="MyVideo"                    // string — unique identifier, used in CLI
  component={MyVideoComponent}   // React.FC — the video component
  durationInFrames={150}          // number — total frames
  fps={30}                        // number — frames per second
  width={1920}                    // number — pixels
  height={1080}                   // number — pixels
  schema={zodSchema}              // ZodSchema (optional) — for parameterized rendering
  defaultProps={{}}               // object (optional) — default input props
  calculateMetadata={fn}          // function (optional) — dynamic duration/props
/>
```

### `<Sequence>`

Time-shifts children — child's frame 0 starts at `from`:

```tsx
import { Sequence } from "remotion";

<Sequence
  from={30}                     // number — global frame when sequence starts
  durationInFrames={60}         // number (optional) — how long sequence lasts
  name="Intro"                  // string (optional) — label in Studio timeline
  layout="none"                 // "none" (optional) — don't wrap in positioned div
/>
```

### `<Series>`

Stack sequences back-to-back:

```tsx
import { Series } from "remotion";

<Series>
  <Series.Sequence durationInFrames={60} offset={0}>
    <ChildA />
  </Series.Sequence>
  <Series.Sequence durationInFrames={90} offset={-15}>
    <ChildB />    {/* Starts 15 frames before ChildA ends */}
  </Series.Sequence>
</Series>
```

The `offset` prop shifts the start relative to when it would naturally start (negative = overlap with previous).

### `<Folder>`

Organize compositions in Studio sidebar (no rendering effect):

```tsx
import { Folder } from "remotion";

<Folder name="Social Videos">
  <Composition id="Short" ... />
  <Composition id="Reel" ... />
</Folder>
```

### `<Still>`

Register a single-frame composition (for thumbnails, posters):

```tsx
import { Still } from "remotion";

<Still
  id="Thumbnail"
  component={ThumbnailComponent}
  width={1280}
  height={720}
  defaultProps={{ title: "My Video" }}
/>
```

## Transition Components

```bash
npm i @remotion/transitions
```

### TransitionSeries

```tsx
import { TransitionSeries, linearTiming, springTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import { slide } from "@remotion/transitions/slide";
import { wipe } from "@remotion/transitions/wipe";
import { flip } from "@remotion/transitions/flip";
import { clockWipe } from "@remotion/transitions/clock-wipe";

<TransitionSeries>
  <TransitionSeries.Sequence durationInFrames={90}>
    <SceneA />
  </TransitionSeries.Sequence>
  <TransitionSeries.Transition
    presentation={fade()}
    timing={linearTiming({ durationInFrames: 30 })}
  />
  <TransitionSeries.Sequence durationInFrames={90}>
    <SceneB />
  </TransitionSeries.Sequence>
</TransitionSeries>
```

### Presentations

```tsx
fade()                                     // Cross-fade
slide({ direction: "from-left" })          // "from-left" | "from-right" | "from-top" | "from-bottom"
wipe({ direction: "from-left" })           // Same directions as slide
flip({ direction: "from-left" })           // 3D flip
clockWipe({ width: 1920, height: 1080 })   // Circular clock wipe
```

### Timings

```tsx
linearTiming({ durationInFrames: 30 })
// Linear interpolation over given frames

springTiming({
  config: { damping: 12, stiffness: 200 },
  durationInFrames: 30, // optional cap
  reverse: false,       // optional
})
```

## Media Components

### `<Img>`

```tsx
import { Img, staticFile } from "remotion";

<Img
  src={staticFile("photo.jpg")}  // string — URL or staticFile()
  style={{}}                      // CSSProperties
  onError={(e) => {}}             // error handler
  // Delays rendering until image is loaded — no layout shift
/>
```

### `<OffthreadVideo>` (Preferred)

```tsx
import { OffthreadVideo, staticFile } from "remotion";

<OffthreadVideo
  src={staticFile("bg.mp4")}     // string — video source
  style={{}}                      // CSSProperties
  volume={1}                      // number | (f: number) => number
  muted={false}                   // boolean
  playbackRate={1}                // number — speed multiplier
  startFrom={0}                   // number — start from this frame of the source
  endAt={150}                     // number — end at this frame of the source
  // Extracts frames off the main thread — more reliable than <Video>
/>
```

### `<Video>` (Legacy)

Same props as `<OffthreadVideo>`. Use only if you need `onError` handling during preview; prefer `<OffthreadVideo>` for rendering.

### `<Audio>`

```tsx
import { Audio, staticFile } from "remotion";

<Audio
  src={staticFile("music.mp3")}  // string — audio source
  volume={1}                      // number | (f: number) => number
  startFrom={0}                   // number — skip first N frames of source
  endAt={300}                     // number — stop at this frame
  muted={false}                   // boolean
  playbackRate={1}                // number
  // Wrap in <Sequence> to control when audio plays
/>
```

### `<IFrame>`

```tsx
import { IFrame } from "remotion";

<IFrame
  src="https://example.com"
  style={{ width: "100%", height: "100%" }}
  // Delays rendering until iframe loads
/>
```

## Utility Functions

### staticFile()

```tsx
import { staticFile } from "remotion";

staticFile("image.png")     // → references public/image.png
staticFile("fonts/inter.woff2")
```

### getInputProps()

```tsx
import { getInputProps } from "remotion";

const props = getInputProps();
// Returns props passed via CLI --props flag or Studio input
// Used outside of component tree (e.g., in Root.tsx)
```

### delayRender() / continueRender()

Pause rendering until async operations complete:

```tsx
import { delayRender, continueRender } from "remotion";
import { useCallback, useEffect, useState } from "react";

export const DataComponent: React.FC = () => {
  const [data, setData] = useState(null);
  const [handle] = useState(() => delayRender("Loading data..."));

  useEffect(() => {
    fetch("https://api.example.com/data")
      .then((res) => res.json())
      .then((json) => {
        setData(json);
        continueRender(handle);
      })
      .catch((err) => {
        console.error(err);
        continueRender(handle);
      });
  }, [handle]);

  if (!data) return null;
  return <div>{JSON.stringify(data)}</div>;
};
```

### random()

Deterministic random number — same seed always produces same value (important for consistent renders):

```tsx
import { random } from "remotion";

const value = random("my-seed");          // number between 0 and 1
const value2 = random(`item-${index}`);   // unique per index but deterministic
```

## Rendering API (Server-Side)

For programmatic rendering from Node.js (e.g., serverless functions, automation):

```tsx
import { bundle } from "@remotion/bundler";
import { renderMedia, selectComposition } from "@remotion/renderer";

// 1. Bundle the project
const bundleLocation = await bundle({
  entryPoint: "./src/index.ts",
  webpackOverride: (config) => config,
});

// 2. Select composition
const composition = await selectComposition({
  serveUrl: bundleLocation,
  id: "MyVideo",
  inputProps: { title: "Hello" },
});

// 3. Render
await renderMedia({
  composition,
  serveUrl: bundleLocation,
  codec: "h264",
  outputLocation: "out/video.mp4",
  inputProps: { title: "Hello" },
});
```

### renderStill()

```tsx
import { renderStill } from "@remotion/renderer";

await renderStill({
  composition,
  serveUrl: bundleLocation,
  output: "out/thumbnail.png",
  frame: 45,
  imageFormat: "png", // "png" | "jpeg" | "webp"
});
```

## Player API

```bash
npm i @remotion/player
```

### Player Props

```tsx
import { Player, PlayerRef } from "@remotion/player";

<Player
  component={MyVideo}              // React.FC
  inputProps={{}}                   // Props for the component
  durationInFrames={150}           // number
  fps={30}                         // number
  compositionWidth={1920}          // number
  compositionHeight={1080}         // number
  style={{}}                       // CSSProperties (for container)
  controls={true}                  // boolean — show play/pause/seek
  autoPlay={false}                 // boolean
  loop={false}                     // boolean
  clickToPlay={true}               // boolean
  doubleClickToFullscreen={true}   // boolean
  spaceKeyToPlayOrPause={true}     // boolean
  moveToBeginningWhenEnded={true}  // boolean
  showVolumeControls={true}        // boolean
  allowFullscreen={true}           // boolean
  numberOfSharedAudioTags={5}      // number
  renderLoading={() => <Loading />} // React.FC (optional)
  errorFallback={({ error }) => <Error />} // React.FC (optional)
/>
```

### Player Ref Methods

```tsx
import { useRef } from "react";
import { PlayerRef } from "@remotion/player";

const playerRef = useRef<PlayerRef>(null);

playerRef.current?.play();
playerRef.current?.pause();
playerRef.current?.toggle();
playerRef.current?.seekTo(45);              // Seek to frame 45
playerRef.current?.getCurrentFrame();       // Get current frame
playerRef.current?.isPlaying();             // boolean
playerRef.current?.getVolume();             // 0-1
playerRef.current?.setVolume(0.5);
playerRef.current?.isMuted();
playerRef.current?.mute();
playerRef.current?.unmute();
playerRef.current?.requestFullscreen();
playerRef.current?.exitFullscreen();

// Events
playerRef.current?.addEventListener("play", () => {});
playerRef.current?.addEventListener("pause", () => {});
playerRef.current?.addEventListener("ended", () => {});
playerRef.current?.addEventListener("seeked", (e) => { e.detail.frame });
playerRef.current?.addEventListener("frameupdate", (e) => { e.detail.frame });
playerRef.current?.addEventListener("fullscreenchange", (e) => { e.detail.isFullscreen });
```

## Additional Packages

| Package | Purpose | Install |
|---------|---------|---------|
| `@remotion/media-utils` | `getVideoMetadata()`, `getAudioDuration()`, `useAudioData()`, `visualizeAudio()` | `npm i @remotion/media-utils` |
| `@remotion/layout-utils` | `measureText()` — measure text dimensions before rendering | `npm i @remotion/layout-utils` |
| `@remotion/motion-blur` | `<CameraMotionBlur>` — wrap components for motion blur effect | `npm i @remotion/motion-blur` |
| `@remotion/google-fonts` | `loadFont()` — load any Google Font with type-safe API | `npm i @remotion/google-fonts` |
| `@remotion/gif` | `<Gif>` — render animated GIFs frame-synced | `npm i @remotion/gif` |
| `@remotion/paths` | SVG path manipulation — `parsePath()`, `interpolatePath()`, `evolvePath()` | `npm i @remotion/paths` |
| `@remotion/shapes` | `<Rect>`, `<Circle>`, `<Triangle>`, `<Ellipse>`, `<Star>`, `<Pie>` | `npm i @remotion/shapes` |
| `@remotion/noise` | `noise2D()`, `noise3D()`, `noise4D()` — Perlin noise for organic animations | `npm i @remotion/noise` |
| `@remotion/lottie` | `<Lottie>` — render Lottie/Bodymovin animations | `npm i @remotion/lottie` |
| `@remotion/rive` | `<Rive>` — render Rive animations | `npm i @remotion/rive` |
| `@remotion/three` | `<ThreeCanvas>` — Three.js integration for 3D scenes | `npm i @remotion/three` |
| `@remotion/lambda` | Serverless rendering on AWS Lambda | `npm i @remotion/lambda` |
| `@remotion/cloudrun` | Serverless rendering on Google Cloud Run | `npm i @remotion/cloudrun` |
| `@remotion/tailwind` | Tailwind CSS integration for Remotion | `npm i @remotion/tailwind` |
