def lemmy_accuracy(lemmatizer, X, y):
    total = 0
    correct = 0
    ambiguous = 0

    for index, target in enumerate(y):
        word_class, full_form = X[index]
        predicted = lemmatizer.lemmatize(word_class, full_form)
        total += 1
        if len(predicted) > 1:
            ambiguous += 1
        elif predicted[0] == target:
            correct += 1
        
    print("correct:", correct)
    print("ambiguous:", ambiguous)
    print("total:", total)
    print("accuracy:", correct / total)
    print("ambiguous%:", ambiguous / total)
    print("ambiguous + accuracy:", (ambiguous + correct) / total)
