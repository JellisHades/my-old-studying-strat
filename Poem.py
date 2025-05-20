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
	IncorrectAnswers = []
	Index = 0

	for Answer in Answers:
		if Answer == "" or Answer == "poem":
			continue

		Index += 1
		Input = input(str(Index) + ": ")
		
		IsCorrect = SimplifyText(Input) == SimplifyText(Answer)
		
		if not IsCorrect:
			print("Correct Answer: " + Answer)
			IncorrectAnswers.append(Answer)

			if not ContinueOnMistake:
				break
	
	return IncorrectAnswers, Index

if __name__ == "__main__":
	from Answers import Answers
	import os

	Answers = Answers.split("\n")
	
	while True:
		os.system("cls")
		IncorrectAnswers, Questions = Start(Answers)

		print(f'{Questions - len(IncorrectAnswers)}/{Questions}')
		input()