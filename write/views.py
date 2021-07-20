from django.shortcuts import render
from .models import Notes
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import IntegrityError


# Create your views here.
@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
def note(request):
    # By using this method,we can get the required notes
    if request.method == 'GET':
        note_id = request.GET.get('note_id', None)
        if note_id is None:
            content = {
                'message': 'note_id is missing'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        try:
            note_info = Notes.objects.get(id=note_id)
            content = {
                'notes': note_info.notes,
                "created_at": note_info.created_at,
                'updated_at': note_info.updated_at

            }
            return Response(content, status=status.HTTP_200_OK)
        except Notes.DoesNotExist:
            content = {
                'message': 'note_id is invalid'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            content = {
                'message': 'note_id should be a integer'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'POST':
        # With this request,we can add new notes
        notes = request.POST.get('notes', None)
        if notes is None:
            content = {
                'message': 'notes is mandatory '
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        try:
            new_notes = Notes.objects.create(
                notes=notes

            )
            new_notes.save()
            content = {
                'message': "new notes has been added",
                'data': {
                    'notes_id': new_notes.id,
                    'notes': new_notes.notes,
                    "created_at": new_notes.created_at,
                    'updated_at': new_notes.updated_at
                }
            }
            return Response(content, status=status.HTTP_201_CREATED)

        except Notes.DoesNotExist:
            content = {
                'message': 'note_id is invalid'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        # With this method,we can edit the list of notes
        new_notes = request.POST.get('notes', None)
        note_id = request.POST.get("note_id", None)

        if note_id is None:
            content = {
                'message': ' note_id is mandatory'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        try:
            note_info = Notes.objects.get(id=note_id)
            note_info.notes = new_notes if new_notes is not None else note_info.notes
            note_info.save()
            content = {
                'message': " notes has been updated",
                'data': {
                    'note_id': note_info.id,
                    'notes': note_info.notes,
                }

            }
            return Response(content, status=status.HTTP_200_OK)

        except Notes.DoesNotExist:
            content = {
                'message': 'note_id  is invalid'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        note_id = request.POST.get('note_id', None)
        if note_id is None:
            content = {
                'message': 'note_id is mandatory'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        try:
            note_info = Notes.objects.get(id=note_id)
            note_info.delete()
            content = {
                'message': 'notes has been deleted'
            }
            return Response(content, status=status.HTTP_200_OK)
        except Notes.DoesNotExist:
            content = {
                'message': 'note_id is invalid'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            content = {
                'message': 'note_id should be a integer'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def notes_details(request):
    note_id = request.GET.get('note_id', None)
    # with this method, we can get all the notes or else we can get single note
    if note_id is None:
        all_notes = Notes.objects.all()

    elif note_id is not None:
        try:
            all_notes = Notes.objects.filter(id=note_id)
        except ValueError:
            content = {
                'message': 'note_id should be a integer'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
    final_notes = []
    for temp_note in all_notes:
        content = {
            'notes_id': temp_note.id,
            'notes': temp_note.notes,
            "created_at": temp_note.created_at,
            'updated_at': temp_note.updated_at
        }
        final_notes.append(content)

    return Response(final_notes, status=status.HTTP_200_OK)
