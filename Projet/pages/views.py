from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from .models import Evénement
from django.contrib.auth import login ,authenticate
from users.models import CustomUser
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _  # For translations
from django.utils.translation import gettext_lazy as _
from .models import Evénement , participation  ,CoAuteur ,Invitation ,Evaluation ,Affectation ,Encheres ,Presentation ,Guide
from .forms import EvénementForm,soumissionForm ,CoAuteurForm ,InvitationForm ,EvaluationForm ,EncheresForm ,CameraReadyForm , PrsenatationForm ,GuideForm
from users.forms import CustomUserForm 
from django.contrib.auth.models import Group
import json
from .models import soumission
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.utils import timezone
from datetime import datetime








# Create your views here.


def index(request):
    return render(request, 'pages/index.html')

def aide(request):
    return render(request,'pages/aide.html')

@login_required
def commun(request):
    user = request.user
    
    # Récupérez tous les événements auxquels l'utilisateur participe
    events = Evénement.objects.filter(participation__user=user)
    
    # Créer une liste pour stocker les rôles de l'utilisateur dans chaque événement
    roles_for_events = []
    
    # Boucle à travers les événements
    for event in events:
        # Récupérer les participations de l'utilisateur pour cet événement
        participations = participation.objects.filter(evenement=event, user=user)
        
        # Créer une liste pour stocker les rôles de l'utilisateur dans cet événement
        roles_for_event = []
        
        # Boucle à travers les participations de l'utilisateur pour cet événement
        for part in participations:
            # Ajoutez les rôles ayant la valeur True à la liste
            if part.organisateur:
                roles_for_event.append("Organisateur")
            if part.evaluateur:
                roles_for_event.append("Évaluateur")
            if part.auteur:
                roles_for_event.append("Auteur")
            if part.speaker:
                roles_for_event.append("Speaker")
            if part.editeur:
                roles_for_event.append("Éditeur")
        
        # Si des rôles sont trouvés pour cet événement, ajoutez-les à la liste des rôles pour les événements
        if roles_for_event:
            roles_for_events.append({'event': event, 'roles': roles_for_event})
    
    return render(request, 'pages/commun.html', {'roles_for_events': roles_for_events})


def connexion(request):
    
     if request.method=="POST":
            
            action=request.POST.get('action',None)

            if action=='login':
                email_cnx=request.POST['email_cnx']
                motDePasse_cnx=request.POST['motDePasse_cnx']

                try:
                    utilisateur = CustomUser.objects.get(email=email_cnx)
                except CustomUser.DoesNotExist:
                    utilisateur = None

                # authenticate user
                utilisateur = authenticate(request, username=email_cnx, password=motDePasse_cnx)
                
                # Vérification du mot de passe si l'utilisateur existe
                if utilisateur is not None and utilisateur.check_password(motDePasse_cnx):
                    login(request, utilisateur)
                    return redirect('commun')
                else:
                    messages.error(request, 'Identifiants invalides.')
                        
            elif action == 'register':
                  nom=request.POST['nom']
                  prenom=request.POST['prenom']
                  organisation=request.POST['organisation']
                  pays=request.POST['pays']
                  email = request.POST['email']
                  motDePasse = request.POST['motDePasse']
                  password_conf=request.POST['password_conf']

                  if motDePasse != password_conf:
                        messages.error(request, 'Les mots de passe ne correspondent pas.')
                  else:
                        mon_utilisateur = CustomUser.objects._create_user(email, password=motDePasse)
                        
                        mon_utilisateur.nom=nom
                        mon_utilisateur.prenom=prenom
                        mon_utilisateur.pays=pays
                        mon_utilisateur.organisation=organisation
                        mon_utilisateur.is_active = True
                        mon_utilisateur.save()
                        activation_link = f'http://http://127.0.0.1:8000/connexion'
            
                        # Send email with activation link
                        send_mail(
                            'Activation de compte',
                            f'Bonjour {prenom} {nom}, veuillez cliquer sur le lien suivant pour activer votre compte: {activation_link}',
                            'settings.EMAIL_HOST_USER',
                            [email],
                            fail_silently=False
                        )
                        return redirect('connexion')
    
     return render(request,'pages/connexion.html')


@login_required
def modifier_profil(request ,my_id ):
    user = request.user
    # Essayer de récupérer l'utilisateur à partir de son id, s'il n'existe pas, retourner une 404
    obj = get_object_or_404(CustomUser, id=user.id)
    form = CustomUserForm(request.POST or None, instance=obj)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
    return render(request, 'pages/profilForm.html', {'form': form})# Rediriger vers la page de profil après enregistrement des modifications
@login_required
def supprimer_profil(request,my_id):
    user = request.user
    # Essayer de récupérer l'utilisateur à partir de son id, s'il n'existe pas, retourner une 404
    obj = get_object_or_404(CustomUser, id=user.id)
    if request.method == "POST":
            obj.delete()
            redirect('connexion')
    return render(request,'pages/deleteProfil.html')
@login_required
def listEvnt(request):
    search_criteria = request.GET.get('search_criteria')
    query = request.GET.get('q')

    events = Evénement.objects.all()

    if search_criteria and query:
        filter_args = {search_criteria + '__icontains': query}
        events = events.filter(**filter_args)

    for event in events:
        guide = Guide.objects.filter(evenement=event).first()
        if guide:
            event.guide_soumission = guide.guide_soumission
        else:
            event.guide_soumission = "Aucun guide associé"

    return render(request, 'pages/listeEvnt.html', {'events': events})

@login_required
def affiche_guide_org(request,evenement_id):
    evenement = get_object_or_404(Evénement, id=evenement_id)
    guide = Guide.objects.filter(evenement=evenement).first()
    return render(request, 'pages/affiche_guide_org.html', {'guide': guide,'evenement':evenement})

                   


@login_required
def creation(request):
              form= EvénementForm(request.POST or None)
              if request.method == 'POST':
                if form.is_valid():
                  event_instance = form.save()
                  participation_instance = participation.objects.create(
                   evenement=event_instance,
                   user=request.user,
                   organisateur=True
                   )
                  organisateur_group = Group.objects.get(name='organisateur')
                  organisateur_group.user_set.add(request.user)
                return redirect('commun') 
              else:
                 event_form = EvénementForm()
              return render(request,'pages/create.html' , {'form':form})
    
"""def Accueil_Organisateur(request):
    evnt =Evénement.objects.all()
    return render(request,'pages/Acceuil_Organisation.html',{'evnt':evnt} )
"""
@login_required
def modifier_Accueil_Organisateur(request,my_id):
    obj = Evénement.objects.get(id=my_id )
    form= EvénementForm(request.POST or None , instance=obj)
    if request.method == 'POST':
        if form.is_valid():
                form.save()
    return render(request,'pages/Accueil_Organisateur.html', {'form':form , 'obj':obj}  )
@login_required
def supprimer_Accueil_Organisateur(request,my_id):
      evnt=get_object_or_404(Evénement,id=my_id)
      form= EvénementForm(request.POST or None , instance=evnt)
      if request.method == "POST":
            evnt.delete()
            redirect('commun')
      return render(request,'pages/confirmer_suppre_evnt.html',  {'form':form , 'evnt':evnt})
            
@login_required
def submission(request, evenement_id):
    evenement = get_object_or_404(Evénement, id=evenement_id)
    if request.method == 'POST':
        form_soum = soumissionForm(request.POST, request.FILES)
        
        if form_soum.is_valid():
            soumission_instance = form_soum.save(commit=False)
            soumission_instance.user = request.user
            soumission_instance.evenement = evenement
            soumission_instance.save()

            # Vérifier s'il existe déjà une participation pour cet utilisateur et cet événement
            existing_participation = participation.objects.filter(user=request.user, evenement=evenement).first()
            if existing_participation:
                # Mettre à jour le rôle de la participation existante
                existing_participation.auteur = True
                existing_participation.save()
            else:
                # Créer une nouvelle instance de Participation avec le rôle auteur
                participation.objects.create(user=request.user, evenement=evenement, auteur=True)

            # Enregistrer les co-auteurs
            coauteurs_json = request.POST.get('coauteurs')  # Récupérer les données des co-auteurs au format JSON
            coauteurs_list = json.loads(coauteurs_json) if coauteurs_json else []  # Convertir en liste Python
            
            for coauteur_data in coauteurs_list:
                CoAuteur.objects.create(
                    email_co_auteur=coauteur_data['email'],
                    prenom_coauteur=coauteur_data['prenom'],
                    nom_coauteur=coauteur_data['nom'],
                    soumission=soumission_instance
                )
            
             # Envoyer un email aux co-auteurs
                subject = "Vous êtes co-auteur dans une nouvelle soumission"
                message = f"Bonjour {coauteur_data['prenom']} {coauteur_data['nom']},\n\n" \
                          f"Vous avez été ajouté en tant que co-auteur dans la soumission '{soumission_instance.titre}' " \
                          f"pour l'événement '{evenement.nom_evnt}'.\n\n" \
                          "Cordialement,\nL'équipe de l'événement"
                recipient_list = [coauteur_data['email']]
                send_mail(subject, message, 'anfelmami6@gmail.com', recipient_list)
            return redirect('commun')
    else:
        form_soum = soumissionForm()
    
    return render(request, 'pages/submissionForm.html', {'form_soum': form_soum, 'evenement': evenement})
@login_required
def modifier_soumission(request, evenement_id, soumission_id):
    evenement_obj = get_object_or_404(Evénement, id=evenement_id)

    # Récupération de la soumission spécifique à modifier
    soumission_obj = get_object_or_404(soumission, id=soumission_id, evenement=evenement_obj)

    # Récupération des coauteurs associés à cette soumission
    coauteurs = CoAuteur.objects.filter(soumission=soumission_obj)

    if request.method == 'POST':
        form_soum = soumissionForm(request.POST, request.FILES, instance=soumission_obj)
        form_coauteur = CoAuteurForm(request.POST)

        if form_soum.is_valid() and form_coauteur.is_valid():
            soumission_instance = form_soum.save()

            # Suppression des coauteurs existants avant d'ajouter les nouveaux
            CoAuteur.objects.filter(soumission=soumission_instance).delete()

            coauteurs_json = request.POST.get('coauteurs')
            coauteurs_list = json.loads(coauteurs_json) if coauteurs_json else []
            
            for email in coauteurs_list:
                CoAuteur.objects.create(email_co_auteur=email, soumission=soumission_instance)

            return redirect('commun')  # Redirection après soumission réussie
    else:
        form_soum = soumissionForm(instance=soumission_obj)
        form_coauteur = CoAuteurForm(initial={'coauteurs': [coauteur.email_co_auteur for coauteur in coauteurs]})

    return render(request, 'pages/submissionForm.html', {'form_soum': form_soum, 'form_coauteur': form_coauteur})


@login_required
def Acceuil_Evaluateur(request):
     
     return render(request, 'pages/Accueil_evaluateur.html')


@login_required
def delete_soumission(request, soumission_id):
    soumissions = get_object_or_404(soumission, id=soumission_id)
    evenement_id = soumissions.evenement.id
    if request.method == 'POST':
        soumissions.delete()
        messages.success(request, 'La soumission a été supprimée avec succès.')
        return redirect(reverse('liste_soumissions', args=[evenement_id]))
    return redirect(reverse('liste_soumissions', args=[evenement_id]))


@login_required
def liste_soumissions(request, evenement_id):
    utilisateur_courant = request.user
    evenement = get_object_or_404(Evénement, id=evenement_id)
    soumissions = soumission.objects.filter(user=utilisateur_courant, evenement=evenement)
  
    # Récupérer les co-auteurs pour chaque soumission
    for soum in soumissions:
        soum.evenement_date_fin_soumission = soum.evenement.date_fin_soumission
        soum.coauteurs = CoAuteur.objects.filter(soumission=soum)
        



    # Récupérer la date et l'heure actuelles
    today = timezone.now().date()
    current_time = datetime.now()
 

    context = {
        'soumissions': soumissions,
        'evenement': evenement,
        'today': today,
        'current_time': current_time,
    }
    return render(request, 'pages/liste_soumissions.html', context)

@login_required
def details_soumission(request, evenement_id, soumission_id):
    soumissions = get_object_or_404(soumission, id=soumission_id, evenement_id=evenement_id)
    evaluations = Evaluation.objects.filter(soumission=soumissions)
    return render(request, 'pages/details_soumission.html', {'soumission': soumissions, 'evaluations': evaluations})

@login_required
def invitation_view(request, evenement_id):
    evnt = get_object_or_404(Evénement, id=evenement_id)
    current_user = request.user  # Get the current logged-in user

    if request.method == 'POST':
        form = InvitationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email_invitation']
            
            # Vérifier si l'email existe dans la table CustomUser
            User = get_user_model()
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                # Ajouter un message d'erreur
                messages.error(request, 'Cet email n\'appartient à aucun utilisateur.')
            else:
                # Si l'utilisateur existe, enregistrer l'invitation
                invitation = form.save(commit=False)
                invitation.user = current_user  # Set the user to the currently logged-in user
                invitation.evenement = evnt  # Set the event to the current event
                invitation.save()
    else:
        form = InvitationForm()

    return render(request, 'pages/AddMbrForm.html', {'form': form, 'evnt': evnt})

@login_required
def liens(request,evenement_id):
    evenement_obj = get_object_or_404(Evénement, id=evenement_id)
    user = request.user

    return render(request, 'pages/href.html' ,{ 'evenement_obj': evenement_obj})

@login_required
def mes_invitations(request):
    current_user = request.user
    # Filtrer les invitations où email_invitation correspond à l'email du user courant
    invitations = Invitation.objects.filter(email_invitation=current_user.email)

    if request.method == 'POST':
        invitation_id = request.POST.get('invitation_id')
        action = request.POST.get('action')
        if invitation_id and action == 'accept':
            try:
                invitation = Invitation.objects.get(id=invitation_id, email_invitation=current_user.email)
                invitation.accepted = True
                invitation.save()

                # Chercher ou créer une instance de Participation
                participations, created = participation.objects.get_or_create(
                    user=current_user,
                    evenement=invitation.evenement
                )

                # Mettre à jour le rôle spécifique
                if not created:
                    setattr(participations, invitation.role, True)
                else:
                    setattr(participations, invitation.role, True)
                participations.save()

                messages.success(request, 'Invitation acceptée et participation créée/mise à jour avec succès.')
            except Invitation.DoesNotExist:
                messages.error(request, 'Invitation non trouvée.')
            except TypeError as e:
                messages.error(request, f'Erreur: {e}')

    return render(request, 'pages/listeinv.html', {'invitations': invitations})

@login_required
def evaluer(request, evenement_id, soumission_id):
    evnt = get_object_or_404(Evénement, id=evenement_id)
    soumissions = get_object_or_404(soumission, id=soumission_id)

    current_user = request.user  # Get the current logged-in user

    if request.method == 'POST':
        form = EvaluationForm(request.POST)
        if form.is_valid():
            evaluation = form.save(commit=False)
            evaluation.user = current_user  # Set the user to the currently logged-in user
            evaluation.soumission = soumissions  # Set the submission to the current submission
            evaluation.save()
            
            # Update the status of the submission to True
            soumissions.status = True
            soumissions.save()

            # Redirect to a success page or whatever you want
            return redirect('commun')
    else:
        form = EvaluationForm()

    return render(request, 'pages/EvaluationForm.html', {'form': form})
@login_required
def modifier_evaluation(request, evenement_id, soumission_id):
    evenement = get_object_or_404(Evénement, id=evenement_id)
    soumissions = get_object_or_404(soumission, id=soumission_id, evenement=evenement)
    evaluation = get_object_or_404(Evaluation, soumission=soumissions, user=request.user)

    if request.method == 'POST':
        form = EvaluationForm(request.POST, instance=evaluation)
        if form.is_valid():
            form.save()
            return redirect('commun')  # Redirect to appropriate view after modification
    else:
        form = EvaluationForm(instance=evaluation)

    return render(request, 'pages/modifier_evaluation.html', {'form': form, 'evenement': evenement, 'soumission': soumissions})
@login_required
def supprimer_evaluation(request, evenement_id, soumission_id):
    evenement = get_object_or_404(Evénement, id=evenement_id)
    soumissions = get_object_or_404(soumission, id=soumission_id, evenement=evenement)
    evaluation = get_object_or_404(Evaluation, soumission=soumissions, user=request.user)

    if request.method == 'POST':
        evaluation.delete()
        # Update the status of the submission to False
        soumissions.status = False
        soumissions.save()
        return redirect(reverse('affectation_ev', kwargs={'evenement_id': evenement.id}))

    return render(request, 'pages/supprimer_evaluation.html', {'evaluation': evaluation, 'evenement': evenement, 'soumission': soumissions})

@login_required
def liensEv(request, evenement_id):
    evenement_obj = get_object_or_404(Evénement, id=evenement_id)
    user = request.user

    return render(request, 'pages/liensEv.html' ,{ 'evenement_obj': evenement_obj})
@login_required
def liens_aut(request, evenement_id):
    evenement_obj = get_object_or_404(Evénement, id=evenement_id)
    user = request.user

    return render(request, 'pages/liens_aut.html' ,{ 'evenement_obj': evenement_obj})
@login_required
def soumissions_par_evenement(request, evenement_id):
    evenement = get_object_or_404(Evénement, id=evenement_id)
    soumissions = soumission.objects.filter(evenement=evenement)
    evaluateurs = participation.objects.filter(evenement=evenement, evaluateur=True)
    coauteurs = CoAuteur.objects.filter(soumission__in=soumissions)
    
    if request.method == 'POST':
        soumission_id = request.POST.get('soumission_id')
        evaluateur_ids = request.POST.getlist(f'evaluateur_ids_{soumission_id}')
       
        
        if soumission_id and evaluateur_ids:
            soumission_obj = get_object_or_404(soumission, id=soumission_id)
            for evaluateur_id in evaluateur_ids:
                evaluateur = get_object_or_404(CustomUser, id=evaluateur_id)
                Affectation.objects.create(user=evaluateur, soumission=soumission_obj)
            messages.success(request, 'Affectations enregistrées avec succès.')
            return redirect('affectation', evenement_id=evenement.id)

    return render(request, 'pages/soumissions_par_evenement.html', {
        'soumissions': soumissions,
        'evaluateurs': evaluateurs,
        'coauteurs': coauteurs,
        'evenement': evenement
    })
    



@login_required
def affectation(request, evenement_id):
    evenement = get_object_or_404(Evénement, id=evenement_id)
    soumissions = soumission.objects.filter(evenement=evenement)
    affectations = Affectation.objects.filter(soumission__in=soumissions)

    context = {
        'affectations': affectations,
        'evenement': evenement,
    }
    return render(request, 'pages/affectation.html', context)

@login_required
def affectation_ev(request, evenement_id):
    evenement = Evénement.objects.get(id=evenement_id)
    user = request.user
    affectations = Affectation.objects.filter(user=user)
    soumissions = [affectation.soumission for affectation in affectations if affectation.soumission.evenement == evenement]
    context = {
        'evenement': evenement,
        'soumissions': soumissions
    }
    return render(request, 'pages/affectation_ev.html', context)

@login_required
def afficher_encheres(request, evenement_id):
    # Récupérer l'événement correspondant à l'ID fourni
    evenement = Evénement.objects.get(id=evenement_id)

    soumissions = soumission.objects.filter(evenement=evenement)
    choix_enthousiasme = Encheres.e

    if request.method == 'POST':
        # Récupérer les données du formulaire soumis
        soumission_id = request.POST.get('soumission_id')
        enthousiasme = request.POST.get('enthousiasme')

        # Enregistrer l'enthousiasme dans la base de données
        Encheres.objects.create(
            user=request.user,
            soumission_id=soumission_id,
            enthousiasme=enthousiasme
        )
      

    return render(request, 'pages/encheres.html', {'soumissions': soumissions, 'est_evenement_courant': evenement , 'choix_enthousiasme': choix_enthousiasme})


@login_required
def liste_encheres(request, evenement_id):
    evenement = get_object_or_404(Evénement, id=evenement_id)
    encheres = Encheres.objects.filter(soumission__evenement=evenement)

    # Organiser les enchères par soumission
    encheres_par_soumission = {}
    for enchere in encheres:
        if enchere.soumission.id not in encheres_par_soumission:
            encheres_par_soumission[enchere.soumission.id] = {
                'titre': enchere.soumission.titre,
                'resume':  enchere.soumission.resume,
                'encheres': []
            }
        encheres_par_soumission[enchere.soumission.id]['encheres'].append(enchere)

    context = {
        'evenement': evenement,
        'encheres_par_soumission': encheres_par_soumission
    }

    return render(request, 'pages/liste_encheres.html', context)

@login_required
def liste_evaluation_org(request, evenement_id):
    evenement = get_object_or_404(Evénement, id=evenement_id)
    evaluations = Evaluation.objects.filter(soumission__evenement=evenement)

    # Organiser les évaluations par soumission
    evaluations_par_soumission = {}
    for evaluation in evaluations:
        if evaluation.soumission.id not in evaluations_par_soumission:
            evaluations_par_soumission[evaluation.soumission.id] = {
                'titre': evaluation.soumission.titre,
                'resume': evaluation.soumission.resume,
                'accept': evaluation.soumission.accept,
                'camera_ready_zip': evaluation.soumission.camera_ready_zip,
                'camera_ready_pdf': evaluation.soumission.camera_ready_pdf,
                'evaluations': []
            }
        evaluations_par_soumission[evaluation.soumission.id]['evaluations'].append(evaluation)

    context = {
        'evenement': evenement,
        'evaluations_par_soumission': evaluations_par_soumission
    }

    if request.method == 'POST':
        soumission_id = request.POST.get('soumission_id')
        new_accept_value = request.POST.get('accept')
        # Convertir la chaîne de caractères en booléen
        new_accept_value = new_accept_value.lower() == 'true'
        soumissions = get_object_or_404(soumission, id=soumission_id)
        soumissions.accept = new_accept_value
        soumissions.save()
        return redirect('liste_evaluation_org', evenement_id=evenement_id)

    return render(request, 'pages/liste_evaluation_org.html', context)

@login_required
def somissions_acceptees(request, evenement_id):
    evenement_courant = get_object_or_404(Evénement, id=evenement_id)
    soumissions = soumission.objects.filter(evenement=evenement_courant, accept=True)
    
    if request.method == 'POST':
        form = CameraReadyForm(request.POST, request.FILES)
        if form.is_valid():
            soumission_id = form.cleaned_data['soumission_id']
            soumissions = get_object_or_404(soumission, id=soumission_id)
            soumissions.camera_ready_pdf = form.cleaned_data['camera_ready_pdf']
            soumissions.camera_ready_zip = form.cleaned_data['camera_ready_zip']
            soumissions.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = CameraReadyForm()

    return render(request, 'pages/somissions_acceptees.html', {'soumissions': soumissions, 'form': form})

@login_required
def speaker(request, evenement_id):
    current_user = request.user
    current_event = get_object_or_404(Evénement, id=evenement_id)

    # Vérifier si l'utilisateur a une participation avec le rôle de speaker
    participations = get_object_or_404(participation, user=current_user, evenement=current_event)

    if participations.speaker:
        try:
            presentation = Presentation.objects.get(user=current_user, evenement=current_event)
            return render(request, 'pages/presentation.html', {'presentation': presentation})
        except Presentation.DoesNotExist:
            if request.method == 'POST':
                form = PrsenatationForm(request.POST)
                if form.is_valid():
                    presentation = form.save(commit=False)
                    presentation.user = current_user
                    presentation.evenement = current_event
                    presentation.save()
                    return redirect('presentation_detail', presentation_id=presentation.id)
            else:
                form =PrsenatationForm()
            return render(request, 'pages/speaker.html', {'form': form, 'event': current_event})
@login_required
def presentation_detail(request, presentation_id):
    presentation = get_object_or_404(Presentation, id=presentation_id)
    return render(request, 'pages/presentation.html', {'presentation': presentation})


@login_required
def modifier_presentation(request, presentation_id):
    presentation = get_object_or_404(Presentation, id=presentation_id, user=request.user)
    
    if request.method == 'POST':
        form = PrsenatationForm(request.POST, instance=presentation)
        if form.is_valid():
            form.save()
            messages.success(request, 'Présentation mise à jour avec succès.')
            return redirect('presentation_detail', presentation_id=presentation.id)
    else:
        form = PrsenatationForm(instance=presentation)
    
    return render(request, 'pages/modifier_presentation.html', {'form': form, 'presentation': presentation})

@login_required
def supprimer_presentation(request, presentation_id):
    presentation = get_object_or_404(Presentation, id=presentation_id, user=request.user)
    
    if request.method == 'POST':
        presentation.delete()
        messages.success(request, 'Présentation supprimée avec succès.')
        return redirect('commun')  # Rediriger vers une vue appropriée après suppression
    
    return render(request, 'pages/confirmer_suppression.html', {'presentation': presentation})


@login_required
def statistics(request, evenement_id):
    evenement = get_object_or_404(Evénement, id=evenement_id)
    submissions = soumission.objects.filter(evenement=evenement)
    evaluations = Evaluation.objects.filter(soumission__in=submissions)
    encheres = Encheres.objects.filter(soumission__in=submissions)

    submissions_by_country = submissions.values('user__pays').annotate(total=Count('id')).order_by('-total')

    total_invitations = Invitation.objects.filter(evenement=evenement).count()
    accepted_invitations = Invitation.objects.filter(evenement=evenement, accepted=True).count()
    evaluator_assignments = Affectation.objects.filter(soumission__evenement=evenement).values('user__nom', 'user__prenom').annotate(total=Count('id')).order_by('-total') 


    total_acceptees = soumission.objects.filter(evenement=evenement,accept=True).count()
    total_refusees = soumission.objects.filter(evenement=evenement,accept=False).count()
    context = {
        "submissions": submissions,
        "evaluations": evaluations,
        "encheres": encheres,
        "submissions_by_country": submissions_by_country,
        "total_invitations": total_invitations,
        "accepted_invitations": accepted_invitations,
        "evaluator_assignments": evaluator_assignments,
        "total_acceptees":total_acceptees,
        "total_refusees":total_refusees
    }
    return render(request, 'pages/statistics.html', context)
@login_required
def liste_speakers(request, evenement_id):
    evenement = Evénement.objects.get(pk=evenement_id)
    presentations = Presentation.objects.filter(evenement=evenement)

    return render(request, 'pages/listeSpeaker.html', {'evenement': evenement, 'presentations': presentations})
@login_required
def ajouter_guide(request, evenement_id):
    current_user = request.user
    evenement = Evénement.objects.get(pk=evenement_id)

    participations = get_object_or_404(participation, user=current_user, evenement=evenement)

    if participations.editeur:
        try:
            guide = Guide.objects.get(user=current_user, evenement=evenement)
            return render(request, 'pages/guide.html', {'guide': guide})
        except Guide.DoesNotExist:
           if request.method == 'POST':
                 form = GuideForm(request.POST)
                 if form.is_valid():
                    guide = form.save(commit=False)
                    guide.user = request.user
                    guide.evenement = evenement
                    guide.save()
                    return redirect('guide_detail' , guide_id=guide.id)  # Remplacez par la vue de votre page de succès
           else:
                 form = GuideForm()
    return render(request, 'pages/ajouter_guide.html', {'form': form})


@login_required
def guide_detail(request, guide_id):
    guide = get_object_or_404(Guide, id=guide_id)
    return render(request, 'pages/guide.html', {'guide': guide})


@login_required
def modifier_guide(request, guide_id):
    guide = get_object_or_404(Guide, id=guide_id, user=request.user)
    
    if request.method == 'POST':
        form = GuideForm(request.POST, instance=guide)
        if form.is_valid():
            form.save()
            messages.success(request, 'Présentation mise à jour avec succès.')
            return redirect('guide_detail', guide_id=guide.id)
    else:
        form = GuideForm(instance=guide)
    
    return render(request, 'pages/modifier_guide.html', {'form': form, 'guide': guide})

@login_required
def supprimer_guide(request, guide_id):
    guide = get_object_or_404(Guide, id=guide_id, user=request.user)
    
    if request.method == 'POST':
        guide.delete()
        messages.success(request, 'Présentation supprimée avec succès.')
        return redirect('commun')  # Rediriger vers une vue appropriée après suppression
    
    return render(request, 'pages/confirmer_suppression_guide.html', {'guide': guide})
@login_required
def custom_logout_view(request):
    logout(request)
    return redirect('index') 