import ActivityHandler


class CustomPromptBot(ActivityHandler):
    def __init__(self, conversation_state: ConversationState, user_state: UserState):
        if conversation_state is None:
            raise TypeError(
                "[CustomPromptBot]: Missing parameter. conversation_state is required but None was given"
            )
        if user_state is None:
            raise TypeError(
                "[CustomPromptBot]: Missing parameter. user_state is required but None was given"
            )

        self.conversation_state = conversation_state
        self.user_state = user_state


async def on_message_activity(self, turn_context: TurnContext):
    # Get the state properties from the turn context.
    profile = await self.profile_accessor.get(turn_context, UserProfile)
    flow = await self.flow_accessor.get(turn_context, ConversationFlow)


# Save changes to UserState and ConversationState
