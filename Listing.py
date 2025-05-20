import random

ContinueOnMistake = False

SpecialCharacters = False
SpaceSensitive = False
CaseSensitive = False

Alphabet = "abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"

def RemoveSpecialCharacters(Str):
	NewStr = ""
	
	for i in range(len(Str)):
		Char = Str[i]
		
		if Char in Alphabet:
			NewStr += Char
	
	return NewStr

def SimplifyText(Text):
	Text = Text
	Text = SpecialCharacters and Text or RemoveSpecialCharacters(Text)
	Text = SpaceSensitive and Text.replace(" ", "") or Text
	Text = not CaseSensitive and Text.lower() or Text
	Text = Text.replace(" ", "")

	return Text

def Start(Answers):
	Answers = Answers.copy()

	QuestionsTouched = 0
	IncorrectAnswers = []

	for v in range(len(Answers)):
		i = int(random.random() * len(Answers))
		RemainingAnswers = Answers[i][0].copy()
		QuestionsTouched += len(RemainingAnswers)

		print(f'{v + 1}. {Answers[i][1]}')
		
		while len(RemainingAnswers) > 0:
			Input = SimplifyText(input("	Answer: "))

			IsCorrect = False

			for CorrectAnswer in RemainingAnswers:
				if Input == SimplifyText(CorrectAnswer):
					IsCorrect = True

					RemainingAnswers.remove(CorrectAnswer)
			
			if not IsCorrect: break
	    
		del Answers[i]

		if len(RemainingAnswers) > 0:
			print("	Correct answers:")
			for CorrectAnswer in RemainingAnswers:
				IncorrectAnswers.append(CorrectAnswer)
				print("		" + CorrectAnswer)

	return IncorrectAnswers, QuestionsTouched

if __name__ == "__main__":
	import os
	
	while True:
		os.system("cls")
		from Answers import Answers
		IncorrectAnswers, Questions = Start(Answers)

		print(f'{Questions - len(IncorrectAnswers)}/{Questions}')
		input()