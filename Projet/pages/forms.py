from django import forms
from .models import Evénement,soumission,CoAuteur, Evaluation ,Invitation ,Encheres , Presentation ,Guide
from users.models import CustomUser


class EvénementForm (forms.ModelForm):
    class Meta:
        model = Evénement
        fields = [
                'nom_evnt',
                'acronym',
                'type',
                'date_debut_evnt',
                'date_fin_evnt',
                'description',
                'pays',
                'ville',
                'addresse',
                'date_debut_soumission',
                'date_fin_soumission',
                'date_debut_enchere',
                'date_fin_enchere',
            ]
        widgets = {
            'nom_evnt': forms.TextInput(attrs={'class': 'element input'}),
            'acronym': forms.Textarea(attrs={'class': 'element input'}),
            'type': forms.Select(attrs={'class': 'element select'}),
            'date_debut_evnt': forms.DateInput(attrs={'class': 'element input', 'type': 'date'}),
            'date_fin_evnt': forms.DateInput(attrs={'class': 'element input', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'element input'}),
            'pays': forms.Select(attrs={'class': 'element select'}),
            'ville': forms.TextInput(attrs={'class': 'element input'}),
            'addresse': forms.TextInput(attrs={'class': 'element input'}),
            'date_debut_soumission':forms.DateInput(attrs={'class': 'element input', 'type': 'date'}),
            'date_fin_soumission':forms.DateInput(attrs={'class': 'element input', 'type': 'date'}),
            'date_debut_enchere':forms.DateInput(attrs={'class': 'element input', 'type': 'date'}),
            'date_fin_enchere':forms.DateInput(attrs={'class': 'element input', 'type': 'date'}),
        }

class EventSearchForm(forms.Form):
    search_query = forms.CharField(label='Recherche', required=False)

class soumissionForm (forms.ModelForm):
    class Meta:
        model = soumission
        fields = [
                'titre',
                'resume',
                'contrat',
            ]
        widgets = {
            'contrat': forms.FileInput(attrs={'accept': '.pdf'}),
        }
class CameraReadyForm(forms.Form):
    soumission_id = forms.IntegerField(widget=forms.HiddenInput())
    camera_ready_pdf = forms.FileField(required=False, label='Camera Ready PDF')
    camera_ready_zip = forms.FileField(required=False, label='Camera Ready ZIP')


class CoAuteurForm (forms.ModelForm):
    class Meta:
        model = CoAuteur
        fields = ['email_co_auteur' , 'nom_coauteur'  , 'prenom_coauteur' ]

    def __init__(self, *args, **kwargs):
        super(CoAuteurForm, self).__init__(*args, **kwargs)
        self.fields['email_co_auteur'].required = False  # Rendre le champ facultatif
        self.fields['nom_coauteur'].required = False
        self.fields['prenom_coauteur'].required = False

class EvaluationForm (forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ['commentaire','maitrise','note','commentaire_confidentiel' ]


class InvitationForm (forms.ModelForm):
    class Meta:
        model = Invitation
        fields = ['email_invitation','role' ]


class EncheresForm(forms.ModelForm):
    class Meta:
        model = Encheres
        fields=['enthousiasme']

class PrsenatationForm(forms.ModelForm):
    class Meta:
        model = Presentation
        fields=['titre_pres','affiliation_pres','biographie_pres']

class GuideForm(forms.ModelForm):
    class Meta:
        model = Guide
        fields=['guide_soumission']