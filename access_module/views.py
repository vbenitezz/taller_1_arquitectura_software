#from django.shortcuts import render, redirect
#from django.contrib.auth import login
#from .forms import Custom_User_Creation_Form

#def register(request):
#    if request.method == 'POST':
#        form = Custom_User_Creation_Form(request.POST)
#        if form.is_valid():
#            user = form.save()
#            login(request, user)
 #           if user.user_type == 'company':
 #               return redirect('inventory')
#            else:
#                return redirect('home')  
#    else:
 #       form = Custom_User_Creation_Form()
#    return render(request, 'register.html', {'form': form})
