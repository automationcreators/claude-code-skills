# Remotion Project Templates

Complete starter templates for common video types. Each template includes a Root.tsx registration, the main component, and a Zod schema for parameterized rendering.

## 1. YouTube Short / Social Vertical (1080x1920, 9:16)

Vertical video for YouTube Shorts, Instagram Reels, or TikTok.

### Schema & Component

```tsx
// src/schemas/short.ts
import { z } from "zod";

export const shortSchema = z.object({
  title: z.string(),
  subtitle: z.string().optional(),
  hook: z.string().describe("Opening hook text shown first"),
  bodyLines: z.array(z.string()).default([]),
  accentColor: z.string().default("#ff3366"),
  backgroundColor: z.string().default("#0a0a0a"),
});

export type ShortProps = z.infer<typeof shortSchema>;
```

```tsx
// src/Short.tsx
import { useCurrentFrame, useVideoConfig, interpolate, spring, Sequence } from "remotion";
import type { ShortProps } from "./schemas/short";

const Hook: React.FC<{ text: string; color: string }> = ({ text, color }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const scale = spring({ frame, fps, config: { damping: 10, stiffness: 150 } });
  const opacity = interpolate(frame, [0, 10], [0, 1], { extrapolateRight: "clamp" });

  return (
    <div
      style={{
        fontSize: 64,
        fontWeight: 900,
        color,
        textAlign: "center",
        transform: `scale(${scale})`,
        opacity,
        padding: "0 60px",
        lineHeight: 1.2,
      }}
    >
      {text}
    </div>
  );
};

const BodyContent: React.FC<{ lines: string[] }> = ({ lines }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 24, padding: "0 60px" }}>
      {lines.map((line, i) => {
        const progress = spring({
          frame: frame - i * 10,
          fps,
          config: { damping: 14, stiffness: 160 },
        });

        return (
          <div
            key={i}
            style={{
              fontSize: 40,
              color: "white",
              opacity: progress,
              transform: `translateY(${(1 - progress) * 30}px)`,
            }}
          >
            {line}
          </div>
        );
      })}
    </div>
  );
};

export const Short: React.FC<ShortProps> = ({
  title,
  subtitle,
  hook,
  bodyLines,
  accentColor,
  backgroundColor,
}) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  const fadeOut = interpolate(
    frame,
    [durationInFrames - 15, durationInFrames],
    [1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        backgroundColor,
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        gap: 40,
        opacity: fadeOut,
      }}
    >
      <Sequence from={0} durationInFrames={60}>
        <Hook text={hook} color={accentColor} />
      </Sequence>

      <Sequence from={45}>
        <div style={{ textAlign: "center" }}>
          <div style={{ fontSize: 52, fontWeight: "bold", color: "white" }}>{title}</div>
          {subtitle && (
            <div style={{ fontSize: 32, color: "rgba(255,255,255,0.6)", marginTop: 12 }}>
              {subtitle}
            </div>
          )}
        </div>
      </Sequence>

      {bodyLines.length > 0 && (
        <Sequence from={75}>
          <BodyContent lines={bodyLines} />
        </Sequence>
      )}
    </div>
  );
};
```

### Root.tsx Registration

```tsx
<Composition
  id="Short"
  component={Short}
  durationInFrames={270}  // 9 seconds at 30fps
  fps={30}
  width={1080}
  height={1920}
  schema={shortSchema}
  defaultProps={{
    title: "5 Automation Tips",
    hook: "Stop wasting time on manual tasks",
    bodyLines: ["Use n8n for workflows", "Automate with AI", "Scale everything"],
    accentColor: "#ff3366",
    backgroundColor: "#0a0a0a",
  }}
/>
```

---

## 2. Presentation / Slide Deck (1920x1080, 16:9)

Slide-based presentation with transitions between slides.

### Schema & Component

```tsx
// src/schemas/presentation.ts
import { z } from "zod";

const slideSchema = z.discriminatedUnion("type", [
  z.object({
    type: z.literal("title"),
    title: z.string(),
    subtitle: z.string().optional(),
  }),
  z.object({
    type: z.literal("bullets"),
    heading: z.string(),
    items: z.array(z.string()),
  }),
  z.object({
    type: z.literal("quote"),
    text: z.string(),
    attribution: z.string().optional(),
  }),
  z.object({
    type: z.literal("image"),
    heading: z.string(),
    imageSrc: z.string(),
  }),
]);

export const presentationSchema = z.object({
  slides: z.array(slideSchema),
  accentColor: z.string().default("#3b82f6"),
  fontFamily: z.string().default("Inter, system-ui, sans-serif"),
});

export type PresentationProps = z.infer<typeof presentationSchema>;
export type Slide = z.infer<typeof slideSchema>;
```

```tsx
// src/Presentation.tsx
import {
  useCurrentFrame, useVideoConfig, interpolate, spring, Easing,
} from "remotion";
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { slide } from "@remotion/transitions/slide";
import type { PresentationProps, Slide } from "./schemas/presentation";

const FRAMES_PER_SLIDE = 150; // 5 seconds
const TRANSITION_FRAMES = 20;

const TitleSlide: React.FC<{ title: string; subtitle?: string; accentColor: string }> = ({
  title, subtitle, accentColor,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const titleScale = spring({ frame, fps, config: { damping: 12, stiffness: 150 } });

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        backgroundColor: "#111",
        gap: 20,
      }}
    >
      <h1
        style={{
          fontSize: 72,
          fontWeight: "bold",
          color: "white",
          transform: `scale(${titleScale})`,
          textAlign: "center",
          padding: "0 100px",
        }}
      >
        {title}
      </h1>
      {subtitle && (
        <p
          style={{
            fontSize: 32,
            color: accentColor,
            opacity: interpolate(frame, [15, 30], [0, 1], { extrapolateRight: "clamp" }),
          }}
        >
          {subtitle}
        </p>
      )}
    </div>
  );
};

const BulletsSlide: React.FC<{
  heading: string;
  items: string[];
  accentColor: string;
}> = ({ heading, items, accentColor }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        backgroundColor: "#111",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        padding: "0 120px",
        gap: 40,
      }}
    >
      <h2 style={{ fontSize: 52, fontWeight: "bold", color: accentColor }}>{heading}</h2>
      <div style={{ display: "flex", flexDirection: "column", gap: 24 }}>
        {items.map((item, i) => {
          const progress = spring({
            frame: frame - 10 - i * 8,
            fps,
            config: { damping: 15, stiffness: 160 },
          });
          return (
            <div
              key={i}
              style={{
                fontSize: 36,
                color: "white",
                opacity: progress,
                transform: `translateX(${(1 - progress) * 40}px)`,
              }}
            >
              {item}
            </div>
          );
        })}
      </div>
    </div>
  );
};

const QuoteSlide: React.FC<{ text: string; attribution?: string }> = ({
  text, attribution,
}) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 25], [0, 1], { extrapolateRight: "clamp" });

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        backgroundColor: "#111",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        padding: "0 150px",
        opacity,
      }}
    >
      <p style={{ fontSize: 44, color: "white", fontStyle: "italic", textAlign: "center", lineHeight: 1.5 }}>
        &ldquo;{text}&rdquo;
      </p>
      {attribution && (
        <p style={{ fontSize: 28, color: "rgba(255,255,255,0.5)", marginTop: 30 }}>
          &mdash; {attribution}
        </p>
      )}
    </div>
  );
};

const SlideRenderer: React.FC<{ slide: Slide; accentColor: string }> = ({
  slide: s, accentColor,
}) => {
  switch (s.type) {
    case "title":
      return <TitleSlide title={s.title} subtitle={s.subtitle} accentColor={accentColor} />;
    case "bullets":
      return <BulletsSlide heading={s.heading} items={s.items} accentColor={accentColor} />;
    case "quote":
      return <QuoteSlide text={s.text} attribution={s.attribution} />;
    case "image":
      return (
        <div style={{ width: "100%", height: "100%", backgroundColor: "#111" }}>
          <h2 style={{ fontSize: 48, color: "white", padding: "60px 100px 0" }}>{s.heading}</h2>
        </div>
      );
  }
};

export const Presentation: React.FC<PresentationProps> = ({ slides, accentColor }) => {
  return (
    <TransitionSeries>
      {slides.flatMap((s, i) => {
        const elements = [
          <TransitionSeries.Sequence key={`slide-${i}`} durationInFrames={FRAMES_PER_SLIDE}>
            <SlideRenderer slide={s} accentColor={accentColor} />
          </TransitionSeries.Sequence>,
        ];

        if (i < slides.length - 1) {
          elements.push(
            <TransitionSeries.Transition
              key={`transition-${i}`}
              presentation={slide({ direction: "from-right" })}
              timing={linearTiming({ durationInFrames: TRANSITION_FRAMES })}
            />
          );
        }

        return elements;
      })}
    </TransitionSeries>
  );
};
```

### Root.tsx Registration

```tsx
<Composition
  id="Presentation"
  component={Presentation}
  fps={30}
  width={1920}
  height={1080}
  schema={presentationSchema}
  defaultProps={{
    slides: [
      { type: "title", title: "Building with AI", subtitle: "A practical guide" },
      { type: "bullets", heading: "Key Takeaways", items: ["Automate first", "Iterate fast", "Ship often"] },
      { type: "quote", text: "The best code is no code at all.", attribution: "Jeff Atwood" },
    ],
    accentColor: "#3b82f6",
    fontFamily: "Inter, system-ui, sans-serif",
  }}
  calculateMetadata={({ props }) => ({
    durationInFrames: props.slides.length * FRAMES_PER_SLIDE - (props.slides.length - 1) * TRANSITION_FRAMES,
  })}
/>
```

---

## 3. Data Visualization (1920x1080)

Animated bar chart with counters.

### Schema & Component

```tsx
// src/schemas/dataViz.ts
import { z } from "zod";

export const dataVizSchema = z.object({
  title: z.string(),
  subtitle: z.string().optional(),
  bars: z.array(
    z.object({
      label: z.string(),
      value: z.number(),
      color: z.string().optional(),
    })
  ),
  unit: z.string().default(""),
  backgroundColor: z.string().default("#0f172a"),
});

export type DataVizProps = z.infer<typeof dataVizSchema>;
```

```tsx
// src/DataViz.tsx
import { useCurrentFrame, useVideoConfig, interpolate, spring, Easing, Sequence } from "remotion";
import type { DataVizProps } from "./schemas/dataViz";

const DEFAULT_COLORS = ["#3b82f6", "#ef4444", "#22c55e", "#f59e0b", "#8b5cf6", "#ec4899"];

const AnimatedBar: React.FC<{
  label: string;
  value: number;
  maxValue: number;
  color: string;
  unit: string;
  index: number;
}> = ({ label, value, maxValue, color, unit, index }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const progress = spring({
    frame: frame - index * 8,
    fps,
    config: { damping: 15, stiffness: 100, mass: 1 },
  });

  const barWidthPercent = (value / maxValue) * 100;
  const animatedWidth = barWidthPercent * progress;

  const displayValue = interpolate(
    frame,
    [index * 8, index * 8 + 40],
    [0, value],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) }
  );

  return (
    <div style={{ display: "flex", alignItems: "center", gap: 20, width: "100%" }}>
      <div style={{ width: 160, fontSize: 24, color: "rgba(255,255,255,0.8)", textAlign: "right" }}>
        {label}
      </div>
      <div style={{ flex: 1, height: 40, backgroundColor: "rgba(255,255,255,0.05)", borderRadius: 6 }}>
        <div
          style={{
            width: `${animatedWidth}%`,
            height: "100%",
            backgroundColor: color,
            borderRadius: 6,
          }}
        />
      </div>
      <div style={{ width: 100, fontSize: 24, color: "white", fontVariantNumeric: "tabular-nums" }}>
        {Math.round(displayValue)}{unit}
      </div>
    </div>
  );
};

export const DataViz: React.FC<DataVizProps> = ({
  title,
  subtitle,
  bars,
  unit,
  backgroundColor,
}) => {
  const frame = useCurrentFrame();
  const maxValue = Math.max(...bars.map((b) => b.value));

  const titleOpacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: "clamp" });

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        backgroundColor,
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        padding: "80px 120px",
        gap: 50,
      }}
    >
      <div style={{ opacity: titleOpacity }}>
        <h1 style={{ fontSize: 56, fontWeight: "bold", color: "white", margin: 0 }}>{title}</h1>
        {subtitle && (
          <p style={{ fontSize: 28, color: "rgba(255,255,255,0.5)", marginTop: 10 }}>{subtitle}</p>
        )}
      </div>

      <Sequence from={15}>
        <div style={{ display: "flex", flexDirection: "column", gap: 24 }}>
          {bars.map((bar, i) => (
            <AnimatedBar
              key={i}
              label={bar.label}
              value={bar.value}
              maxValue={maxValue}
              color={bar.color ?? DEFAULT_COLORS[i % DEFAULT_COLORS.length]}
              unit={unit}
              index={i}
            />
          ))}
        </div>
      </Sequence>
    </div>
  );
};
```

### Root.tsx Registration

```tsx
<Composition
  id="DataViz"
  component={DataViz}
  durationInFrames={180}
  fps={30}
  width={1920}
  height={1080}
  schema={dataVizSchema}
  defaultProps={{
    title: "Monthly Revenue by Product",
    subtitle: "Q4 2024",
    bars: [
      { label: "Product A", value: 85000 },
      { label: "Product B", value: 62000 },
      { label: "Product C", value: 41000 },
      { label: "Product D", value: 29000 },
    ],
    unit: "$",
    backgroundColor: "#0f172a",
  }}
/>
```

---

## 4. Text-Based Video (1920x1080)

Quotes, lyrics, or text reveals with typewriter effect.

### Schema & Component

```tsx
// src/schemas/textVideo.ts
import { z } from "zod";

export const textVideoSchema = z.object({
  segments: z.array(
    z.object({
      text: z.string(),
      style: z.enum(["typewriter", "fade", "pop"]).default("fade"),
      fontSize: z.number().default(56),
    })
  ),
  backgroundColor: z.string().default("#000000"),
  textColor: z.string().default("#ffffff"),
});

export type TextVideoProps = z.infer<typeof textVideoSchema>;
```

```tsx
// src/TextVideo.tsx
import { useCurrentFrame, useVideoConfig, interpolate, spring, Sequence } from "remotion";
import type { TextVideoProps } from "./schemas/textVideo";

const FRAMES_PER_SEGMENT = 120;

const TypewriterSegment: React.FC<{ text: string; fontSize: number; color: string }> = ({
  text, fontSize, color,
}) => {
  const frame = useCurrentFrame();
  const charsToShow = Math.min(Math.floor(frame / 2), text.length);
  const displayed = text.slice(0, charsToShow);
  const isTyping = charsToShow < text.length;

  return (
    <div style={{ fontSize, color, fontFamily: "monospace", whiteSpace: "pre-wrap", textAlign: "center", padding: "0 120px" }}>
      {displayed}
      <span style={{ opacity: isTyping || frame % 30 < 15 ? 1 : 0 }}>|</span>
    </div>
  );
};

const FadeSegment: React.FC<{ text: string; fontSize: number; color: string }> = ({
  text, fontSize, color,
}) => {
  const frame = useCurrentFrame();

  const opacity = interpolate(frame, [0, 25, FRAMES_PER_SEGMENT - 25, FRAMES_PER_SEGMENT], [0, 1, 1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const translateY = interpolate(frame, [0, 25], [30, 0], {
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        fontSize,
        color,
        opacity,
        transform: `translateY(${translateY}px)`,
        textAlign: "center",
        padding: "0 120px",
        lineHeight: 1.4,
      }}
    >
      {text}
    </div>
  );
};

const PopSegment: React.FC<{ text: string; fontSize: number; color: string }> = ({
  text, fontSize, color,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const scale = spring({ frame, fps, config: { damping: 10, stiffness: 150 } });

  const exitOpacity = interpolate(
    frame,
    [FRAMES_PER_SEGMENT - 20, FRAMES_PER_SEGMENT],
    [1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  return (
    <div
      style={{
        fontSize,
        fontWeight: "bold",
        color,
        transform: `scale(${scale})`,
        opacity: exitOpacity,
        textAlign: "center",
        padding: "0 120px",
      }}
    >
      {text}
    </div>
  );
};

export const TextVideo: React.FC<TextVideoProps> = ({
  segments,
  backgroundColor,
  textColor,
}) => {
  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        backgroundColor,
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      {segments.map((seg, i) => (
        <Sequence key={i} from={i * FRAMES_PER_SEGMENT} durationInFrames={FRAMES_PER_SEGMENT}>
          {seg.style === "typewriter" ? (
            <TypewriterSegment text={seg.text} fontSize={seg.fontSize} color={textColor} />
          ) : seg.style === "pop" ? (
            <PopSegment text={seg.text} fontSize={seg.fontSize} color={textColor} />
          ) : (
            <FadeSegment text={seg.text} fontSize={seg.fontSize} color={textColor} />
          )}
        </Sequence>
      ))}
    </div>
  );
};
```

### Root.tsx Registration

```tsx
<Composition
  id="TextVideo"
  component={TextVideo}
  fps={30}
  width={1920}
  height={1080}
  schema={textVideoSchema}
  defaultProps={{
    segments: [
      { text: "The future belongs to those who automate.", style: "typewriter", fontSize: 52 },
      { text: "Work smarter, not harder.", style: "fade", fontSize: 64 },
      { text: "Start building today.", style: "pop", fontSize: 72 },
    ],
    backgroundColor: "#000000",
    textColor: "#ffffff",
  }}
  calculateMetadata={({ props }) => ({
    durationInFrames: props.segments.length * FRAMES_PER_SEGMENT,
  })}
/>
```

---

## 5. Image Slideshow with Ken Burns (1920x1080)

Crossfading images with pan/zoom and optional captions.

### Schema & Component

```tsx
// src/schemas/slideshow.ts
import { z } from "zod";

export const slideshowSchema = z.object({
  slides: z.array(
    z.object({
      imageSrc: z.string(),
      caption: z.string().optional(),
      zoomStart: z.number().default(1),
      zoomEnd: z.number().default(1.2),
    })
  ),
  framesPerSlide: z.number().default(150),
  transitionFrames: z.number().default(30),
  musicSrc: z.string().optional(),
});

export type SlideshowProps = z.infer<typeof slideshowSchema>;
```

```tsx
// src/Slideshow.tsx
import {
  useCurrentFrame, interpolate, Img, Audio, staticFile,
} from "remotion";
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import type { SlideshowProps } from "./schemas/slideshow";

const SlideshowSlide: React.FC<{
  imageSrc: string;
  caption?: string;
  zoomStart: number;
  zoomEnd: number;
  durationInFrames: number;
}> = ({ imageSrc, caption, zoomStart, zoomEnd, durationInFrames }) => {
  const frame = useCurrentFrame();

  const zoom = interpolate(frame, [0, durationInFrames], [zoomStart, zoomEnd], {
    extrapolateRight: "clamp",
  });

  const panX = interpolate(frame, [0, durationInFrames], [0, -3], {
    extrapolateRight: "clamp",
  });

  const captionOpacity = interpolate(frame, [20, 40], [0, 1], {
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        overflow: "hidden",
        position: "relative",
        backgroundColor: "#000",
      }}
    >
      <Img
        src={imageSrc}
        style={{
          width: "100%",
          height: "100%",
          objectFit: "cover",
          transform: `scale(${zoom}) translateX(${panX}%)`,
        }}
      />
      {caption && (
        <div
          style={{
            position: "absolute",
            bottom: 80,
            left: 0,
            right: 0,
            textAlign: "center",
            opacity: captionOpacity,
          }}
        >
          <span
            style={{
              fontSize: 36,
              color: "white",
              backgroundColor: "rgba(0,0,0,0.6)",
              padding: "12px 32px",
              borderRadius: 8,
            }}
          >
            {caption}
          </span>
        </div>
      )}
    </div>
  );
};

export const Slideshow: React.FC<SlideshowProps> = ({
  slides,
  framesPerSlide,
  transitionFrames,
  musicSrc,
}) => {
  return (
    <>
      {musicSrc && <Audio src={staticFile(musicSrc)} volume={0.5} />}
      <TransitionSeries>
        {slides.flatMap((s, i) => {
          const elements = [
            <TransitionSeries.Sequence key={`slide-${i}`} durationInFrames={framesPerSlide}>
              <SlideshowSlide
                imageSrc={s.imageSrc.startsWith("http") ? s.imageSrc : staticFile(s.imageSrc)}
                caption={s.caption}
                zoomStart={s.zoomStart}
                zoomEnd={s.zoomEnd}
                durationInFrames={framesPerSlide}
              />
            </TransitionSeries.Sequence>,
          ];

          if (i < slides.length - 1) {
            elements.push(
              <TransitionSeries.Transition
                key={`transition-${i}`}
                presentation={fade()}
                timing={linearTiming({ durationInFrames: transitionFrames })}
              />
            );
          }

          return elements;
        })}
      </TransitionSeries>
    </>
  );
};
```

### Root.tsx Registration

```tsx
<Composition
  id="Slideshow"
  component={Slideshow}
  fps={30}
  width={1920}
  height={1080}
  schema={slideshowSchema}
  defaultProps={{
    slides: [
      { imageSrc: "photo1.jpg", caption: "Chapter 1", zoomStart: 1, zoomEnd: 1.2 },
      { imageSrc: "photo2.jpg", caption: "Chapter 2", zoomStart: 1.1, zoomEnd: 1 },
      { imageSrc: "photo3.jpg", zoomStart: 1, zoomEnd: 1.15 },
    ],
    framesPerSlide: 150,
    transitionFrames: 30,
  }}
  calculateMetadata={({ props }) => ({
    durationInFrames:
      props.slides.length * props.framesPerSlide -
      (props.slides.length - 1) * props.transitionFrames,
  })}
/>
```

---

## 6. YouTube Intro/Outro (1920x1080, 3-10 seconds)

Short logo animation with channel name and call-to-action.

### Schema & Component

```tsx
// src/schemas/intro.ts
import { z } from "zod";

export const introSchema = z.object({
  channelName: z.string(),
  tagline: z.string().optional(),
  logoSrc: z.string().optional(),
  accentColor: z.string().default("#ff0000"),
  ctaText: z.string().default("Subscribe & Like"),
  mode: z.enum(["intro", "outro"]).default("intro"),
});

export type IntroProps = z.infer<typeof introSchema>;
```

```tsx
// src/Intro.tsx
import {
  useCurrentFrame, useVideoConfig, interpolate, spring, Img, staticFile,
} from "remotion";
import type { IntroProps } from "./schemas/intro";

export const Intro: React.FC<IntroProps> = ({
  channelName,
  tagline,
  logoSrc,
  accentColor,
  ctaText,
  mode,
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  // Logo spring animation
  const logoScale = spring({
    frame,
    fps,
    config: { damping: 8, stiffness: 120, mass: 0.8 },
  });

  const logoRotation = spring({
    frame,
    fps,
    config: { damping: 15, stiffness: 80 },
    from: -15,
    to: 0,
  });

  // Channel name slides in
  const nameOffset = spring({
    frame: frame - 10,
    fps,
    config: { damping: 14, stiffness: 150 },
  });

  // Tagline fades in
  const taglineOpacity = interpolate(frame, [20, 35], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // CTA for outro
  const ctaProgress = spring({
    frame: frame - 25,
    fps,
    config: { damping: 12, stiffness: 100 },
  });

  // Exit fade
  const exitOpacity = interpolate(
    frame,
    [durationInFrames - 10, durationInFrames],
    [1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        backgroundColor: "#0a0a0a",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        gap: 24,
        opacity: exitOpacity,
      }}
    >
      {/* Logo */}
      {logoSrc && (
        <Img
          src={logoSrc.startsWith("http") ? logoSrc : staticFile(logoSrc)}
          style={{
            width: 120,
            height: 120,
            borderRadius: "50%",
            transform: `scale(${logoScale}) rotate(${logoRotation}deg)`,
          }}
        />
      )}

      {/* Accent line */}
      <div
        style={{
          width: nameOffset * 200,
          height: 4,
          backgroundColor: accentColor,
          borderRadius: 2,
        }}
      />

      {/* Channel name */}
      <div
        style={{
          fontSize: 64,
          fontWeight: "bold",
          color: "white",
          opacity: nameOffset,
          transform: `translateY(${(1 - nameOffset) * 20}px)`,
        }}
      >
        {channelName}
      </div>

      {/* Tagline */}
      {tagline && (
        <div
          style={{
            fontSize: 28,
            color: "rgba(255,255,255,0.6)",
            opacity: taglineOpacity,
          }}
        >
          {tagline}
        </div>
      )}

      {/* CTA (outro only) */}
      {mode === "outro" && (
        <div
          style={{
            marginTop: 30,
            fontSize: 32,
            color: accentColor,
            fontWeight: "bold",
            opacity: ctaProgress,
            transform: `scale(${ctaProgress})`,
          }}
        >
          {ctaText}
        </div>
      )}
    </div>
  );
};
```

### Root.tsx Registration

```tsx
<Composition
  id="Intro"
  component={Intro}
  durationInFrames={120}  // 4 seconds
  fps={30}
  width={1920}
  height={1080}
  schema={introSchema}
  defaultProps={{
    channelName: "My Channel",
    tagline: "Automation & AI Tutorials",
    accentColor: "#ff0000",
    ctaText: "Subscribe & Like",
    mode: "intro",
  }}
/>
<Composition
  id="Outro"
  component={Intro}
  durationInFrames={150}  // 5 seconds
  fps={30}
  width={1920}
  height={1080}
  schema={introSchema}
  defaultProps={{
    channelName: "My Channel",
    tagline: "Thanks for watching!",
    accentColor: "#ff0000",
    ctaText: "Subscribe & Hit the Bell",
    mode: "outro",
  }}
/>
```

---

## Complete Root.tsx Example

Combining all templates into one project:

```tsx
// src/Root.tsx
import { Composition, Folder } from "remotion";
import { Short } from "./Short";
import { shortSchema } from "./schemas/short";
import { Presentation } from "./Presentation";
import { presentationSchema } from "./schemas/presentation";
import { DataViz } from "./DataViz";
import { dataVizSchema } from "./schemas/dataViz";
import { TextVideo } from "./TextVideo";
import { textVideoSchema } from "./schemas/textVideo";
import { Slideshow } from "./Slideshow";
import { slideshowSchema } from "./schemas/slideshow";
import { Intro } from "./Intro";
import { introSchema } from "./schemas/intro";

const FRAMES_PER_SLIDE = 150;
const TRANSITION_FRAMES = 20;
const FRAMES_PER_SEGMENT = 120;

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Folder name="Social">
        <Composition
          id="Short"
          component={Short}
          durationInFrames={270}
          fps={30}
          width={1080}
          height={1920}
          schema={shortSchema}
          defaultProps={{
            title: "5 Automation Tips",
            hook: "Stop wasting time",
            bodyLines: ["Tip 1", "Tip 2", "Tip 3"],
            accentColor: "#ff3366",
            backgroundColor: "#0a0a0a",
          }}
        />
      </Folder>

      <Folder name="Presentations">
        <Composition
          id="Presentation"
          component={Presentation}
          fps={30}
          width={1920}
          height={1080}
          schema={presentationSchema}
          defaultProps={{
            slides: [
              { type: "title", title: "My Talk" },
              { type: "bullets", heading: "Points", items: ["A", "B", "C"] },
            ],
            accentColor: "#3b82f6",
            fontFamily: "Inter, system-ui, sans-serif",
          }}
          calculateMetadata={({ props }) => ({
            durationInFrames:
              props.slides.length * FRAMES_PER_SLIDE -
              (props.slides.length - 1) * TRANSITION_FRAMES,
          })}
        />
      </Folder>

      <Folder name="Data">
        <Composition
          id="DataViz"
          component={DataViz}
          durationInFrames={180}
          fps={30}
          width={1920}
          height={1080}
          schema={dataVizSchema}
          defaultProps={{
            title: "Revenue by Product",
            bars: [
              { label: "A", value: 85000 },
              { label: "B", value: 62000 },
            ],
            unit: "$",
            backgroundColor: "#0f172a",
          }}
        />
      </Folder>

      <Folder name="Text">
        <Composition
          id="TextVideo"
          component={TextVideo}
          fps={30}
          width={1920}
          height={1080}
          schema={textVideoSchema}
          defaultProps={{
            segments: [
              { text: "Hello World", style: "typewriter", fontSize: 56 },
              { text: "Goodbye", style: "fade", fontSize: 64 },
            ],
            backgroundColor: "#000000",
            textColor: "#ffffff",
          }}
          calculateMetadata={({ props }) => ({
            durationInFrames: props.segments.length * FRAMES_PER_SEGMENT,
          })}
        />
      </Folder>

      <Folder name="Slideshow">
        <Composition
          id="Slideshow"
          component={Slideshow}
          fps={30}
          width={1920}
          height={1080}
          schema={slideshowSchema}
          defaultProps={{
            slides: [
              { imageSrc: "photo1.jpg", caption: "Slide 1", zoomStart: 1, zoomEnd: 1.2 },
              { imageSrc: "photo2.jpg", zoomStart: 1.1, zoomEnd: 1 },
            ],
            framesPerSlide: 150,
            transitionFrames: 30,
          }}
          calculateMetadata={({ props }) => ({
            durationInFrames:
              props.slides.length * props.framesPerSlide -
              (props.slides.length - 1) * props.transitionFrames,
          })}
        />
      </Folder>

      <Folder name="YouTube">
        <Composition
          id="Intro"
          component={Intro}
          durationInFrames={120}
          fps={30}
          width={1920}
          height={1080}
          schema={introSchema}
          defaultProps={{
            channelName: "My Channel",
            tagline: "Tutorials",
            accentColor: "#ff0000",
            ctaText: "Subscribe",
            mode: "intro",
          }}
        />
        <Composition
          id="Outro"
          component={Intro}
          durationInFrames={150}
          fps={30}
          width={1920}
          height={1080}
          schema={introSchema}
          defaultProps={{
            channelName: "My Channel",
            tagline: "Thanks for watching!",
            accentColor: "#ff0000",
            ctaText: "Subscribe & Hit the Bell",
            mode: "outro",
          }}
        />
      </Folder>
    </>
  );
};
```

---

## Rendering Cheat Sheet

Quick render commands for all templates:

```bash
# YouTube Short (vertical)
npx remotion render src/index.ts Short out/short.mp4 \
  --props='{"title":"My Short","hook":"Watch this","bodyLines":["Line 1","Line 2"]}'

# Presentation
npx remotion render src/index.ts Presentation out/presentation.mp4 \
  --props='{"slides":[{"type":"title","title":"Hello"},{"type":"bullets","heading":"Points","items":["A","B"]}]}'

# Data Visualization
npx remotion render src/index.ts DataViz out/dataviz.mp4 \
  --props='{"title":"Sales","bars":[{"label":"Q1","value":100},{"label":"Q2","value":150}]}'

# Text Video
npx remotion render src/index.ts TextVideo out/text.mp4 \
  --props='{"segments":[{"text":"Hello World","style":"typewriter"}]}'

# Image Slideshow
npx remotion render src/index.ts Slideshow out/slideshow.mp4

# YouTube Intro
npx remotion render src/index.ts Intro out/intro.mp4 \
  --props='{"channelName":"My Channel","mode":"intro"}'

# YouTube Outro
npx remotion render src/index.ts Outro out/outro.mp4 \
  --props='{"channelName":"My Channel","mode":"outro","ctaText":"Subscribe!"}'

# Common flags
#   --quality=80           JPEG quality
#   --crf=18               Video quality (lower=better)
#   --concurrency=50%      CPU usage
#   --scale=2              2x resolution
#   --codec=vp8            WebM output
#   --codec=gif            GIF output
```
