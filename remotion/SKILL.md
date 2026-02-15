---
name: remotion
description: Guide for creating programmatic videos with Remotion, a React framework for video creation. This skill should be used when users want to build animated video content, create Remotion projects, render video programmatically, or build React-based motion graphics. Covers project scaffolding, animation systems, transitions, media handling, parameterized rendering, and output to MP4/WebM/GIF formats.
---

# Remotion Video Creation Guide

This skill provides comprehensive guidance for building programmatic videos using Remotion — a React framework that lets you create videos using TypeScript, React components, and web technologies.

## Quick Start

### Scaffold a New Project

```bash
npx create-video@latest my-video
cd my-video
npm start       # Launch Remotion Studio (browser preview)
```

### Project Structure

```
my-video/
├── src/
│   ├── Root.tsx              # Register all compositions here
│   ├── MyComposition.tsx     # Your video component
│   └── ...
├── public/                   # Static assets (images, fonts, audio)
├── remotion.config.ts        # Bundler and render config
├── package.json
└── tsconfig.json
```

### First Render

```bash
# Preview in Studio
npm start

# Render to MP4
npx remotion render src/index.ts MyComp out/video.mp4
```

## Core Concepts

### Compositions

A Composition registers a video with its dimensions, frame rate, and duration. All compositions go in `Root.tsx`:

```tsx
// src/Root.tsx
import { Composition } from "remotion";
import { MyVideo } from "./MyVideo";

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="MyVideo"
      component={MyVideo}
      durationInFrames={150}
      fps={30}
      width={1920}
      height={1080}
    />
  );
};
```

### useCurrentFrame() and useVideoConfig()

Every video component reads its current frame and config from hooks:

```tsx
import { useCurrentFrame, useVideoConfig } from "remotion";

export const MyVideo: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames, width, height } = useVideoConfig();

  return (
    <div style={{ fontSize: 80, textAlign: "center" }}>
      Frame {frame} of {durationInFrames} ({fps} fps)
    </div>
  );
};
```

### Understanding Frames

- Remotion renders each frame as a React render — your component is a pure function of the frame number
- At 30fps, frame 0 is t=0s, frame 30 is t=1s, frame 60 is t=2s
- Convert: `seconds * fps = frame`, `frame / fps = seconds`
- There are no timers, intervals, or requestAnimationFrame — just `useCurrentFrame()`

## Animation System

### interpolate()

Map frame numbers to animation values. Always use `extrapolateLeft` and `extrapolateRight` to prevent values from continuing beyond your input range:

```tsx
import { useCurrentFrame, interpolate, Easing } from "remotion";

export const FadeSlideIn: React.FC = () => {
  const frame = useCurrentFrame();

  const opacity = interpolate(frame, [0, 30], [0, 1], {
    extrapolateRight: "clamp",
  });

  const translateY = interpolate(frame, [0, 30], [50, 0], {
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.cubic),
  });

  return (
    <div style={{ opacity, transform: `translateY(${translateY}px)` }}>
      Hello World
    </div>
  );
};
```

### spring()

Physics-based animations that feel natural. Returns a value from 0 to ~1:

```tsx
import { useCurrentFrame, useVideoConfig, spring } from "remotion";

export const PopIn: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const scale = spring({
    frame,
    fps,
    config: {
      damping: 12,
      stiffness: 200,
      mass: 0.5,
    },
  });

  return (
    <div style={{ transform: `scale(${scale})` }}>
      Pop!
    </div>
  );
};
```

### Easing Functions

Common easings available from `remotion`:

| Easing | Use Case |
|--------|----------|
| `Easing.linear` | Constant speed |
| `Easing.ease` | Gentle acceleration/deceleration |
| `Easing.in(Easing.cubic)` | Slow start |
| `Easing.out(Easing.cubic)` | Slow end (most common) |
| `Easing.inOut(Easing.cubic)` | Slow start and end |
| `Easing.bezier(x1, y1, x2, y2)` | Custom curve |

> **CRITICAL: Never use CSS transitions or CSS animations.** Remotion renders each frame independently — CSS transitions between frames cause flickering and broken output. Always use `interpolate()` or `spring()` for all animations.

## Sequences and Timing

### `<Sequence>`

Offset components in time. The `from` prop shifts the child's frame 0 to that point:

```tsx
import { Sequence } from "remotion";

export const MyVideo: React.FC = () => {
  return (
    <div>
      <Sequence from={0} durationInFrames={60}>
        <Title />          {/* Plays frames 0–59 */}
      </Sequence>
      <Sequence from={30} durationInFrames={90}>
        <Subtitle />       {/* Plays frames 30–119, child sees frame 0 at global 30 */}
      </Sequence>
      <Sequence from={60}>
        <MainContent />    {/* Plays from frame 60 to end */}
      </Sequence>
    </div>
  );
};
```

Inside a `<Sequence>`, `useCurrentFrame()` returns the local frame (starts at 0 when the Sequence begins).

### `<Series>`

Stack segments back-to-back automatically — no manual `from` calculations:

```tsx
import { Series } from "remotion";

export const MyVideo: React.FC = () => {
  return (
    <Series>
      <Series.Sequence durationInFrames={60}>
        <Intro />
      </Series.Sequence>
      <Series.Sequence durationInFrames={90} offset={-15}>
        <Middle />     {/* Starts 15 frames before Intro ends (overlap) */}
      </Series.Sequence>
      <Series.Sequence durationInFrames={60}>
        <Outro />
      </Series.Sequence>
    </Series>
  );
};
```

## Transitions

Use `@remotion/transitions` for animated transitions between sequences:

```bash
npm i @remotion/transitions
```

```tsx
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import { slide } from "@remotion/transitions/slide";

export const MyVideo: React.FC = () => {
  return (
    <TransitionSeries>
      <TransitionSeries.Sequence durationInFrames={90}>
        <SlideOne />
      </TransitionSeries.Sequence>
      <TransitionSeries.Transition
        presentation={fade()}
        timing={linearTiming({ durationInFrames: 30 })}
      />
      <TransitionSeries.Sequence durationInFrames={90}>
        <SlideTwo />
      </TransitionSeries.Sequence>
      <TransitionSeries.Transition
        presentation={slide({ direction: "from-left" })}
        timing={linearTiming({ durationInFrames: 20 })}
      />
      <TransitionSeries.Sequence durationInFrames={90}>
        <SlideThree />
      </TransitionSeries.Sequence>
    </TransitionSeries>
  );
};
```

Available presentations: `fade()`, `slide()`, `wipe()`, `flip()`, `clockWipe()`.

## Media Handling

### Images

Use `<Img>` from Remotion (not `<img>`) for proper rendering synchronization:

```tsx
import { Img, staticFile } from "remotion";

// From public/ folder
<Img src={staticFile("photo.jpg")} style={{ width: "100%" }} />

// From URL
<Img src="https://example.com/image.png" />
```

### Video

Use `<OffthreadVideo>` (preferred over `<Video>`) — it's more reliable and handles frame extraction off the main thread:

```tsx
import { OffthreadVideo, staticFile } from "remotion";

<OffthreadVideo src={staticFile("background.mp4")} style={{ width: "100%" }} />
```

### Audio

```tsx
import { Audio, staticFile, interpolate, useCurrentFrame } from "remotion";

export const WithAudio: React.FC = () => {
  const frame = useCurrentFrame();
  const volume = interpolate(frame, [0, 15], [0, 1], {
    extrapolateRight: "clamp",
  });

  return <Audio src={staticFile("music.mp3")} volume={volume} />;
};
```

### staticFile()

References files in the `public/` folder. Always use `staticFile()` instead of relative paths:

```tsx
staticFile("logo.png")       // → public/logo.png
staticFile("fonts/inter.woff2")  // → public/fonts/inter.woff2
```

## Parameterized Rendering

Use Zod schemas to define props that can be passed at render time — enabling automation pipelines:

```tsx
// src/MyVideo.tsx
import { z } from "zod";
import { useCurrentFrame, interpolate } from "remotion";

export const myVideoSchema = z.object({
  title: z.string(),
  subtitle: z.string().optional(),
  accentColor: z.string().default("#0066ff"),
});

type MyVideoProps = z.infer<typeof myVideoSchema>;

export const MyVideo: React.FC<MyVideoProps> = ({
  title,
  subtitle,
  accentColor,
}) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 30], [0, 1], {
    extrapolateRight: "clamp",
  });

  return (
    <div style={{ opacity, color: accentColor }}>
      <h1>{title}</h1>
      {subtitle && <p>{subtitle}</p>}
    </div>
  );
};
```

Register with the schema and default props:

```tsx
// src/Root.tsx
import { Composition } from "remotion";
import { MyVideo, myVideoSchema } from "./MyVideo";

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="MyVideo"
      component={MyVideo}
      durationInFrames={150}
      fps={30}
      width={1920}
      height={1080}
      schema={myVideoSchema}
      defaultProps={{
        title: "Default Title",
        accentColor: "#0066ff",
      }}
    />
  );
};
```

### Dynamic Duration with calculateMetadata()

```tsx
<Composition
  id="MyVideo"
  component={MyVideo}
  fps={30}
  width={1920}
  height={1080}
  schema={myVideoSchema}
  defaultProps={{ title: "Hello", accentColor: "#0066ff" }}
  calculateMetadata={({ props }) => {
    return {
      durationInFrames: props.title.length * 5 + 60,
    };
  }}
/>
```

### Passing Props via CLI

```bash
npx remotion render src/index.ts MyVideo out/video.mp4 \
  --props='{"title": "Custom Title", "accentColor": "#ff0000"}'
```

## Player Component

Embed Remotion videos in React apps without rendering to file:

```bash
npm i @remotion/player
```

```tsx
import { Player } from "@remotion/player";
import { MyVideo } from "./MyVideo";

export const Preview: React.FC = () => {
  return (
    <Player
      component={MyVideo}
      inputProps={{ title: "Live Preview", accentColor: "#0066ff" }}
      durationInFrames={150}
      fps={30}
      compositionWidth={1920}
      compositionHeight={1080}
      style={{ width: 640 }}
      controls
      autoPlay
      loop
    />
  );
};
```

## Rendering Pipeline

### CLI Rendering

```bash
# MP4 (default, requires ffmpeg)
npx remotion render src/index.ts MyComp out/video.mp4

# WebM
npx remotion render src/index.ts MyComp out/video.webm --codec=vp8

# GIF
npx remotion render src/index.ts MyComp out/animation.gif

# PNG sequence
npx remotion render src/index.ts MyComp out/ --image-format=png --sequence

# Audio only
npx remotion render src/index.ts MyComp out/audio.mp3 --codec=mp3

# Still frame
npx remotion still src/index.ts MyComp out/thumbnail.png --frame=45
```

### Output Formats

| Format | Codec Flag | Extension | Notes |
|--------|-----------|-----------|-------|
| MP4 (H.264) | `--codec=h264` (default) | `.mp4` | Best compatibility |
| MP4 (H.265) | `--codec=h265` | `.mp4` | Smaller file, less support |
| WebM (VP8) | `--codec=vp8` | `.webm` | Web-friendly |
| WebM (VP9) | `--codec=vp9` | `.webm` | Better quality than VP8 |
| GIF | `--codec=gif` | `.gif` | Large files, limited colors |
| ProRes | `--codec=prores` | `.mov` | Professional editing |
| MP3 | `--codec=mp3` | `.mp3` | Audio only |
| WAV | `--codec=wav` | `.wav` | Lossless audio |
| AAC | `--codec=aac` | `.aac` | Compressed audio |
| PNG sequence | `--sequence --image-format=png` | `.png` | Lossless frames |
| Transparent | `--codec=vp8 --image-format=png` | `.webm` | Alpha channel |

### Useful CLI Flags

```bash
--concurrency=50%    # Use half CPU cores
--quality=80         # JPEG quality (0-100)
--scale=2            # 2x resolution
--crf=18             # Quality (lower = better, 0-51 for H.264)
--muted              # Skip audio
--env-file=.env      # Load environment variables
```

## Anti-Patterns

| Anti-Pattern | Why It Breaks | Correct Approach |
|---|---|---|
| CSS `transition` / `animation` | Frames render independently — CSS transitions between frames flicker | Use `interpolate()` or `spring()` |
| `useState` for animation state | State resets each frame render | Derive everything from `useCurrentFrame()` |
| `setTimeout` / `setInterval` | Not frame-based — produces inconsistent timing | Use frame math: `frame >= startFrame` |
| `requestAnimationFrame` | Remotion controls the render loop | Use `useCurrentFrame()` |
| Raw `<img>`, `<video>`, `<audio>` | Won't synchronize with Remotion's render pipeline | Use `<Img>`, `<OffthreadVideo>`, `<Audio>` |
| Relative imports for assets | Breaks in render — assets must be in `public/` | Use `staticFile()` |
| Missing extrapolation clamp | Values overshoot beyond input range | Set `extrapolateLeft/Right: "clamp"` |
| Inline `fetch()` without delayRender | Render completes before data loads | Wrap in `delayRender()` / `continueRender()` |

## v5 Breaking Changes (Preview)

If using Remotion v5 (currently in preview):

- `@remotion/cli` replaces the `remotion` package for CLI commands
- `calculateMetadata()` becomes the primary way to set duration (no more `durationInFrames` on `<Composition>` directly in some patterns)
- Some import paths change — check migration guide at remotion.dev/docs/5-0-migration

## Reference Files

For deeper information, consult these reference files in this skill:

- **[API Reference](references/api_reference.md)** — Complete hook, function, and component API with full signatures
- **[Animation Patterns](references/animation_patterns.md)** — 14 copy-paste-ready animation components
- **[Project Templates](references/project_templates.md)** — 6 complete starter templates for common video types (YouTube Shorts, presentations, data viz, slideshows, intros)
