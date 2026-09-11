export type User = {
  id: number;
  name: string;
  email: string;
  is_admin: boolean;
  font_size: string;
  readable_mode: boolean;
  high_contrast: boolean;
  dyslexia_mode: boolean;
};

export type AccessibilityPreferences = Pick<
  User,
  "font_size" | "readable_mode" | "high_contrast" | "dyslexia_mode"
>;
