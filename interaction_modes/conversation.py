from typing import Callable, List
from plantoid_agents.dialogue_agent import PlantoidDialogueAgent
from elevenlabs import play, stream, save
from elevenlabs.client import ElevenLabs
import os
from playsound import playsound
from plantoid_agents.events.speak import Speak


class PlantoidConversation:

    mode_name = 'conversation'

    def __init__(
        self,
        agents: List[PlantoidDialogueAgent],
        selection_function: Callable[[int, List[PlantoidDialogueAgent]], int],
    ) -> None:
        self.agents = agents
        self._step = 0
        self.select_next_speaker = selection_function
        self.last_speaker_idx = 0

    def increment_speaker_idx(self):
        self.last_speaker_idx += 1

    def set_speaker_idx(self, idx: int):
        self.last_speaker_idx = idx

    def reset(self):
        print("\nNew stimulus. Resetting conversation...\n")
        for agent in self.agents:
            agent.reset()

    def inject(self, name: str, message: str):
        """
        Initiates the conversation with a {message} from {name}
        """
        for agent in self.agents:
            agent.receive(name, message)

        # increment time
        self._step += 1

    #todo: need to restore speaking in enunciation, and it's reated to the first turn behavior
            # ENUNCIATE SIMULUS HERE
    def enunciate(self, intro_message: str):
        playsound(os.getcwd()+"/media/cleanse.mp3", block=False)
        print('\n\033[94m' + 'Enunciating: ' + '\033[0m' + '\033[92m' +  f'\n{intro_message}'  + '\033[0m')
        speaker = self.agents[self.last_speaker_idx]
        # print('speaker name === ', speaker.name)
        # print("INTRO MSG = ", intro_message)
        speaker.speak(self.agents, intro_message, use_streaming=False)


        # Speak.stream_audio_response(
        #         Speak,
        #         intro_message,
        #         speaker.get_voice_id(),
        #         speaker.channel_id)


    def step(self) -> tuple[str, str]:
        # 1. choose the next speaker
        speaker_idx = self.select_next_speaker(self._step, self.agents, self.last_speaker_idx)
        self.set_speaker_idx(speaker_idx)
        speaker = self.agents[speaker_idx]

        # human is selected
        if speaker.is_human == True:

            print('\n\n\033[92mHuman selected (' + speaker.name + ')\033[0m')
            # ENUNCIATE SPEAKER NAME HERE
            speaker.speak(self.agents, speaker.name, use_streaming=False)
            message = speaker.listen_for_speech(self.agents, self._step)
        else:

            # 2. next speaker sends message
            message = speaker.send()
            speaker.speak(self.agents, message)

        # 3. everyone receives message
        for receiver in self.agents:
            receiver.receive(speaker.name, message)

        # 4. increment time
        self._step += 1

        return speaker.name, message