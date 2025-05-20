import random
from pydub.playback import play
from pydub import AudioSegment
from gtts import gTTS
from os import path
from os import remove
import atexit
import sys
import threading

ContinueOnMistake = True
RedoPass = ""

TempMP3 = path.join(sys.path[0], "Audio.mp3")

def ClearTempAudio():
	if path.exists(TempMP3):
		remove(TempMP3)

atexit.register(ClearTempAudio)

LoadedWord = None
WordSound = None

def SplitNotes(String):
	Words = String.split(" ")
	NoteIndex = -1
	
	for SplitWord in Words:
		if Words[-1][-1] != ")":
			break

		NoteIndex += 1

		if SplitWord.startswith("("):
			break
	
	Note = ' '.join(Words[NoteIndex:])[1:-1]
	Word = NoteIndex == -1 and String or ' '.join(Words[:NoteIndex])

	if NoteIndex == -1:
		Note = ""

	return Word, Note

def Pronounce(Word):
	global LoadedWord, WordSound

	if LoadedWord != Word:
		Sound = gTTS(text=Word, lang="en")
		Sound.save(TempMP3)

		WordSound = AudioSegment.from_mp3(TempMP3)
	
	LoadedWord = Word
	play(WordSound)

def Start(Answers):
	Answers = Answers.copy()

	QuestionsTouched = 0
	IncorrectAnswers = []

	for v in range(len(Answers)):
		i = int(random.random() * len(Answers))
		QuestionsTouched += 1

		CorrectAnswer, Note = SplitNotes(Answers[i])
		Pronounciation = CorrectAnswer + ".. " + Note

		threading.Thread(target=Pronounce, args=(Pronounciation,)).start()
		Answer = input("Answer: ")
	    
		while Answer == RedoPass:
			threading.Thread(target=Pronounce, args=(Pronounciation,)).start()
			Answer = input("Answer: ")
		
		IsCorrect = Answer.lower() == CorrectAnswer.lower()

		del Answers[i]

		if IsCorrect: 
			continue
		
		IncorrectAnswers.append(CorrectAnswer)
		print("	Correct answer: " + CorrectAnswer)
		if not ContinueOnMistake:
			break
	
	return IncorrectAnswers, QuestionsTouched

if __name__ == "__main__":
	from Answers import Answers
	import os
	
	while True:
		os.system("cls")
		IncorrectAnswers, Questions = Start(Answers)

		print(f'{Questions - len(IncorrectAnswers)}/{len(Answers)}')
		input()