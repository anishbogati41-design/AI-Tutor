export type ExplanationStyle = "SIMPLE" | "DETAILED" | "STEP_BY_STEP";

export type ConversationMessage = {
  id: number;
  conversation_id: number;
  role: "USER" | "ASSISTANT";
  content: string;
  created_at: string;
};

export type Conversation = {
  id: number;
  user_id: number;
  title: string;
  created_at: string;
  updated_at: string;
};

export type ConversationDetail = Conversation & {
  messages: ConversationMessage[];
};
