from django.shortcuts import render, redirect
from .forms import SubjectCreationForm, CardCreationForm, MarkForm
from .models import Subject, Card


def home(request):
    if not request.user.is_authenticated:
        return redirect('Quiz-Home')

    context ={
        'subjects': Subject.objects.filter(user=request.user)
    }
    return render(request, 'FlashCards/flash_cards_home.html', context=context)


def add_new_subject(request):
    if request.method == "POST":
        form = SubjectCreationForm(request.POST)
        if form.is_valid():
            Subject.objects.create(user=request.user, subject=form.cleaned_data['subject'])
            return redirect('Flash-Cards')
    else:
        form = SubjectCreationForm()
    return render(request, 'FlashCards/add.html', {'form': form})


def subject_details(request, subject_id):
    subject = Subject.objects.get(pk=subject_id)
    context = {
        'subject': subject
    }
    return render(request, 'FlashCards/details.html', context=context)


def add_new_card(request, subject_id):
    subject = Subject.objects.get(pk=subject_id)
    if request.method == 'POST':
        form = CardCreationForm(request.POST, request.FILES)
        new_card = form.save(commit=False)
        new_card.subject = subject
        new_card.save()

        return redirect('Subjects-Details', subject_id)
    else:
        form = CardCreationForm()

    context = {
        'form': form
    }

    return render(request, 'FlashCards/add_card.html', context=context)


def view_card(request, card_id, side):
    card = Card.objects.get(pk=card_id)
    subject = card.subject

    if request.method == 'POST':
        form = MarkForm(request.POST)
        if form.is_valid():
            card.marked_as_known = form.cleaned_data['Known']
            card.save()
            return redirect('Subjects-Details', subject.pk)
    else:
        form = MarkForm(initial={'Known': card.marked_as_known})
    context = {
        'form': form,
        'show_front': side,
        'card': card,
        'subject': subject,

    }
    return render(request, 'FlashCards/view_card.html', context=context)


def edit_card(request, card_id):
    card = Card.objects.get(pk=card_id)

    if request.method == 'POST':
        form = CardCreationForm(request.POST, request.FILES, instance=card)
        if form.is_valid():
            form.save()
            return redirect('View-Card', card_id, 1)

    else:
        form = CardCreationForm(instance=card)

    context = {
        'card': card,
        'form': form
    }
    return render(request, 'FlashCards/edit_card.html', context=context)


def practise(request, subject_id):
    subject = Subject.objects.get(pk=subject_id)
    cards = list(subject.card_set.filter(marked_as_known=False))

    context = {
        'subject': subject,
        'cards': cards
    }

    return render(request, 'FlashCards/practise.html', context=context)


def view_known(request, subject_id):
    subject = Subject.objects.get(pk=subject_id)
    cards = list(subject.card_set.filter(marked_as_known=True))

    context = {
        'subject': subject,
        'cards': cards
    }

    return render(request, 'FlashCards/known.html', context=context)
