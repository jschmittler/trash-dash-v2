export type TDInteractionState =
  | 'default'
  | 'hover'
  | 'focus'
  | 'pressed'
  | 'selected'
  | 'disabled'
  | 'locked';

export type TDCharacter = 'trashy' | 'jimothy';

export type TDMotionPrimitive =
  | 'td.lift'
  | 'td.press'
  | 'td.pop'
  | 'td.wiggle'
  | 'td.slideIn'
  | 'td.peelOut'
  | 'td.stamp'
  | 'td.slam'
  | 'td.shake'
  | 'td.swing'
  | 'td.flapOpen'
  | 'td.countUp'
  | 'td.pageShift'
  | 'td.cardReveal'
  | 'td.celebrationBurst';

export interface TDUISettings {
  reducedMotion: boolean;
  inputMode: 'mouse' | 'keyboard' | 'controller' | 'touch';
}

export interface TDButtonModel {
  id: string;
  label: string;
  state: TDInteractionState;
  action: string;
  icon?: string;
}

export interface TDCharacterSelectModel {
  selectedCharacter: TDCharacter;
  confirmed: boolean;
  availableCharacters: TDCharacter[];
}

export interface TDObjectiveModel {
  id: string;
  label: string;
  current?: number;
  target?: number;
  complete: boolean;
}

export interface TDLevelClearModel {
  score: number;
  timeMs?: number;
  collectibles: Record<string, number>;
  objectives: TDObjectiveModel[];
  newRecord?: boolean;
  unlockedIds?: string[];
  animationSkipped: boolean;
}

export interface TDUIMotionAdapter {
  play(target: unknown, primitive: TDMotionPrimitive): Promise<void> | void;
  cancel(target: unknown): void;
  setReducedMotion(enabled: boolean): void;
}


export type TDUIAssetPhase = 'phase-01' | 'phase-02' | 'phase-03' | 'phase-04';

export interface TDUIAssetSource {
  id: string;
  phase: TDUIAssetPhase;
  sourceSheet: string;
  sourceRegion: [number, number, number, number];
  runtimePath?: string;
  runtimeReady: boolean;
  dynamicTextRequired?: boolean;
}

export interface TDUIAnimationSettings extends TDUISettings {
  skipRepeatedHeroSequences: boolean;
  animationScale: number;
}
