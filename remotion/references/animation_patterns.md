# Remotion Animation Patterns

Copy-paste-ready animation components. Each pattern is a self-contained React component using Remotion's frame-based animation system.

## 1. Fade In / Fade Out

```tsx
import { useCurrentFrame, interpolate } from "remotion";

export const FadeIn: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 20], [0, 1], {
    extrapolateRight: "clamp",
  });

  return <div style={{ opacity }}>{children}</div>;
};

export const FadeInOut: React.FC<{
  children: React.ReactNode;
  durationInFrames: number;
}> = ({ children, durationInFrames }) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(
    frame,
    [0, 20, durationInFrames - 20, durationInFrames],
    [0, 1, 1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  return <div style={{ opacity }}>{children}</div>;
};
```

## 2. Slide In (4 Directions)

```tsx
import { useCurrentFrame, interpolate, Easing } from "remotion";

type Direction = "left" | "right" | "top" | "bottom";

export const SlideIn: React.FC<{
  children: React.ReactNode;
  direction?: Direction;
  distance?: number;
  durationInFrames?: number;
}> = ({ children, direction = "left", distance = 100, durationInFrames = 25 }) => {
  const frame = useCurrentFrame();

  const progress = interpolate(frame, [0, durationInFrames], [0, 1], {
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.cubic),
  });

  const transforms: Record<Direction, string> = {
    left: `translateX(${(1 - progress) * -distance}px)`,
    right: `translateX(${(1 - progress) * distance}px)`,
    top: `translateY(${(1 - progress) * -distance}px)`,
    bottom: `translateY(${(1 - progress) * distance}px)`,
  };

  return (
    <div style={{ transform: transforms[direction], opacity: progress }}>
      {children}
    </div>
  );
};
```

## 3. Scale Up (Pop In) with Spring

```tsx
import { useCurrentFrame, useVideoConfig, spring } from "remotion";

export const PopIn: React.FC<{
  children: React.ReactNode;
  delay?: number;
}> = ({ children, delay = 0 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const scale = spring({
    frame: frame - delay,
    fps,
    config: { damping: 12, stiffness: 200, mass: 0.5 },
  });

  return (
    <div
      style={{
        transform: `scale(${scale})`,
        opacity: scale,
      }}
    >
      {children}
    </div>
  );
};
```

## 4. Typewriter Text

```tsx
import { useCurrentFrame } from "remotion";

export const Typewriter: React.FC<{
  text: string;
  framesPerChar?: number;
  showCursor?: boolean;
}> = ({ text, framesPerChar = 2, showCursor = true }) => {
  const frame = useCurrentFrame();

  const charsToShow = Math.min(
    Math.floor(frame / framesPerChar),
    text.length
  );

  const displayedText = text.slice(0, charsToShow);
  const isTyping = charsToShow < text.length;

  return (
    <span style={{ fontFamily: "monospace", fontSize: 48, whiteSpace: "pre" }}>
      {displayedText}
      {showCursor && (
        <span style={{ opacity: isTyping || frame % 30 < 15 ? 1 : 0 }}>|</span>
      )}
    </span>
  );
};
```

## 5. Number Counter

```tsx
import { useCurrentFrame, interpolate, Easing } from "remotion";

export const NumberCounter: React.FC<{
  from?: number;
  to: number;
  durationInFrames?: number;
  decimals?: number;
  prefix?: string;
  suffix?: string;
}> = ({ from = 0, to, durationInFrames = 60, decimals = 0, prefix = "", suffix = "" }) => {
  const frame = useCurrentFrame();

  const value = interpolate(frame, [0, durationInFrames], [from, to], {
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.cubic),
  });

  return (
    <span style={{ fontSize: 72, fontWeight: "bold", fontVariantNumeric: "tabular-nums" }}>
      {prefix}{value.toFixed(decimals)}{suffix}
    </span>
  );
};
```

## 6. Progress Bar

```tsx
import { useCurrentFrame, interpolate, Easing } from "remotion";

export const ProgressBar: React.FC<{
  progress: number; // 0-1
  durationInFrames?: number;
  color?: string;
  height?: number;
  width?: number;
}> = ({ progress, durationInFrames = 45, color = "#0066ff", height = 8, width = 600 }) => {
  const frame = useCurrentFrame();

  const animatedProgress = interpolate(
    frame,
    [0, durationInFrames],
    [0, progress],
    { extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) }
  );

  return (
    <div
      style={{
        width,
        height,
        backgroundColor: "rgba(255,255,255,0.2)",
        borderRadius: height / 2,
        overflow: "hidden",
      }}
    >
      <div
        style={{
          width: `${animatedProgress * 100}%`,
          height: "100%",
          backgroundColor: color,
          borderRadius: height / 2,
        }}
      />
    </div>
  );
};
```

## 7. Parallax Layers

```tsx
import { useCurrentFrame, interpolate } from "remotion";

export const ParallaxLayer: React.FC<{
  children: React.ReactNode;
  speed: number; // 0.5 = slow, 1 = normal, 2 = fast
  direction?: "horizontal" | "vertical";
}> = ({ children, speed, direction = "vertical" }) => {
  const frame = useCurrentFrame();

  const offset = interpolate(frame, [0, 300], [0, -200 * speed], {
    extrapolateRight: "clamp",
  });

  const transform =
    direction === "vertical"
      ? `translateY(${offset}px)`
      : `translateX(${offset}px)`;

  return <div style={{ transform }}>{children}</div>;
};

// Usage: Stack layers with different speeds
// <ParallaxLayer speed={0.3}><Background /></ParallaxLayer>
// <ParallaxLayer speed={0.6}><Midground /></ParallaxLayer>
// <ParallaxLayer speed={1.0}><Foreground /></ParallaxLayer>
```

## 8. Staggered List Items

```tsx
import { useCurrentFrame, useVideoConfig, spring } from "remotion";

export const StaggeredList: React.FC<{
  items: string[];
  staggerDelay?: number;
}> = ({ items, staggerDelay = 5 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
      {items.map((item, index) => {
        const progress = spring({
          frame: frame - index * staggerDelay,
          fps,
          config: { damping: 15, stiffness: 180, mass: 0.8 },
        });

        return (
          <div
            key={index}
            style={{
              opacity: progress,
              transform: `translateX(${(1 - progress) * 40}px)`,
              fontSize: 32,
            }}
          >
            {item}
          </div>
        );
      })}
    </div>
  );
};
```

## 9. Ken Burns (Pan + Zoom on Image)

```tsx
import { useCurrentFrame, interpolate, Img, staticFile } from "remotion";

export const KenBurns: React.FC<{
  src: string;
  zoomStart?: number;
  zoomEnd?: number;
  panX?: number;
  panY?: number;
}> = ({ src, zoomStart = 1, zoomEnd = 1.3, panX = -5, panY = -3 }) => {
  const frame = useCurrentFrame();

  const zoom = interpolate(frame, [0, 150], [zoomStart, zoomEnd], {
    extrapolateRight: "clamp",
  });

  const x = interpolate(frame, [0, 150], [0, panX], {
    extrapolateRight: "clamp",
  });

  const y = interpolate(frame, [0, 150], [0, panY], {
    extrapolateRight: "clamp",
  });

  return (
    <div style={{ overflow: "hidden", width: "100%", height: "100%" }}>
      <Img
        src={src}
        style={{
          width: "100%",
          height: "100%",
          objectFit: "cover",
          transform: `scale(${zoom}) translate(${x}%, ${y}%)`,
        }}
      />
    </div>
  );
};
```

## 10. Lower Third Title Card

```tsx
import { useCurrentFrame, useVideoConfig, interpolate, spring, Easing } from "remotion";

export const LowerThird: React.FC<{
  name: string;
  title: string;
  accentColor?: string;
  durationInFrames?: number;
}> = ({ name, title, accentColor = "#0066ff", durationInFrames = 120 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Bar slides in
  const barWidth = spring({
    frame,
    fps,
    config: { damping: 15, stiffness: 120 },
  });

  // Text fades in after bar
  const textOpacity = interpolate(frame, [10, 25], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Exit animation
  const exitProgress = interpolate(
    frame,
    [durationInFrames - 20, durationInFrames],
    [0, 1],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  const translateY = exitProgress * 80;

  return (
    <div
      style={{
        position: "absolute",
        bottom: 100,
        left: 80,
        transform: `translateY(${translateY}px)`,
        opacity: 1 - exitProgress,
      }}
    >
      {/* Accent bar */}
      <div
        style={{
          width: 4,
          height: `${barWidth * 70}px`,
          backgroundColor: accentColor,
          position: "absolute",
          left: -16,
          top: 0,
        }}
      />
      {/* Name */}
      <div
        style={{
          fontSize: 36,
          fontWeight: "bold",
          color: "white",
          opacity: textOpacity,
        }}
      >
        {name}
      </div>
      {/* Title */}
      <div
        style={{
          fontSize: 24,
          color: "rgba(255,255,255,0.7)",
          opacity: textOpacity,
          marginTop: 4,
        }}
      >
        {title}
      </div>
    </div>
  );
};
```

## 11. Rotate In

```tsx
import { useCurrentFrame, useVideoConfig, spring } from "remotion";

export const RotateIn: React.FC<{
  children: React.ReactNode;
  degrees?: number;
  delay?: number;
}> = ({ children, degrees = 90, delay = 0 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const progress = spring({
    frame: frame - delay,
    fps,
    config: { damping: 12, stiffness: 100 },
  });

  const rotation = (1 - progress) * degrees;

  return (
    <div
      style={{
        transform: `rotate(${rotation}deg) scale(${progress})`,
        opacity: progress,
        transformOrigin: "center center",
      }}
    >
      {children}
    </div>
  );
};
```

## 12. Audio Waveform Visualization

Requires `@remotion/media-utils`:

```bash
npm i @remotion/media-utils
```

```tsx
import { useCurrentFrame, useVideoConfig, Audio, staticFile } from "remotion";
import { useAudioData, visualizeAudio } from "@remotion/media-utils";

export const AudioWaveform: React.FC<{
  audioSrc: string;
  barColor?: string;
  barCount?: number;
}> = ({ audioSrc, barColor = "#0066ff", barCount = 64 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const audioData = useAudioData(audioSrc);
  if (!audioData) return null;

  const visualization = visualizeAudio({
    fps,
    frame,
    audioData,
    numberOfSamples: 256,
  });

  // Sample bars evenly from the visualization
  const step = Math.floor(visualization.length / barCount);
  const bars = Array.from({ length: barCount }, (_, i) =>
    visualization[i * step] ?? 0
  );

  return (
    <>
      <Audio src={audioSrc} />
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          gap: 2,
          height: 200,
        }}
      >
        {bars.map((amplitude, i) => (
          <div
            key={i}
            style={{
              width: 4,
              height: `${Math.max(amplitude * 200, 2)}px`,
              backgroundColor: barColor,
              borderRadius: 2,
            }}
          />
        ))}
      </div>
    </>
  );
};
```

## 13. Color Interpolation

```tsx
import { useCurrentFrame, interpolateColors } from "remotion";

export const ColorShift: React.FC<{
  children: React.ReactNode;
  colors: string[];
  framesPerColor?: number;
}> = ({ children, colors, framesPerColor = 30 }) => {
  const frame = useCurrentFrame();

  const inputRange = colors.map((_, i) => i * framesPerColor);

  const backgroundColor = interpolateColors(frame, inputRange, colors);

  return (
    <div
      style={{
        backgroundColor,
        width: "100%",
        height: "100%",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      {children}
    </div>
  );
};

// Usage:
// <ColorShift colors={["#1a1a2e", "#16213e", "#0f3460", "#e94560"]}>
//   <h1>Dynamic Background</h1>
// </ColorShift>
```

## 14. Full Scene Combination Example

Combining multiple patterns into a complete scene:

```tsx
import { useCurrentFrame, useVideoConfig, interpolate, spring, Sequence } from "remotion";

const Title: React.FC<{ text: string }> = ({ text }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const scale = spring({
    frame,
    fps,
    config: { damping: 10, stiffness: 150 },
  });

  return (
    <h1
      style={{
        fontSize: 80,
        fontWeight: "bold",
        color: "white",
        textAlign: "center",
        transform: `scale(${scale})`,
      }}
    >
      {text}
    </h1>
  );
};

const Subtitle: React.FC<{ text: string }> = ({ text }) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 20], [0, 1], {
    extrapolateRight: "clamp",
  });
  const translateY = interpolate(frame, [0, 20], [20, 0], {
    extrapolateRight: "clamp",
  });

  return (
    <p
      style={{
        fontSize: 36,
        color: "rgba(255,255,255,0.8)",
        textAlign: "center",
        opacity,
        transform: `translateY(${translateY}px)`,
      }}
    >
      {text}
    </p>
  );
};

const BulletPoints: React.FC<{ items: string[] }> = ({ items }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 20, paddingLeft: 60 }}>
      {items.map((item, i) => {
        const progress = spring({
          frame: frame - i * 8,
          fps,
          config: { damping: 15, stiffness: 180 },
        });

        return (
          <div
            key={i}
            style={{
              fontSize: 28,
              color: "white",
              opacity: progress,
              transform: `translateX(${(1 - progress) * 30}px)`,
            }}
          >
            {item}
          </div>
        );
      })}
    </div>
  );
};

export const FullScene: React.FC = () => {
  const frame = useCurrentFrame();

  const bgOpacity = interpolate(frame, [0, 15], [0, 1], {
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        backgroundColor: "#1a1a2e",
        opacity: bgOpacity,
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        gap: 30,
      }}
    >
      <Sequence from={0} durationInFrames={120}>
        <Title text="Build Videos with Code" />
      </Sequence>

      <Sequence from={15} durationInFrames={105}>
        <Subtitle text="React + TypeScript + Remotion" />
      </Sequence>

      <Sequence from={35} durationInFrames={85}>
        <BulletPoints
          items={[
            "Frame-perfect animations",
            "Parameterized rendering",
            "Programmatic video at scale",
          ]}
        />
      </Sequence>
    </div>
  );
};
```
