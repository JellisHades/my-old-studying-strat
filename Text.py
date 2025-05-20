import random

ContinueOnMistake = True

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
		QuestionsTouched += 1

		print(f'{v + 1}. {Answers[i][1]}')

		CorrectAnswer = Answers[i][0]
		Answer = input("	Answer: ")

		if SimplifyText(Answer) == SimplifyText(CorrectAnswer):
			del Answers[i] 
			continue
		
		IncorrectAnswers.append(Answers[i].copy())
		print("		Correct answer: " + CorrectAnswer)

		del Answers[i]

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