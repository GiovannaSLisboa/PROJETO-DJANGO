from django import forms
from .models import Evento, Ingresso
from django.forms.models import inlineformset_factory


class EventoForm(forms.ModelForm):
    # Opcional: ajustar o tipo de input para data_evento
    data_evento = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label='Data e Hora do Evento'
    )

    class Meta:
        model = Evento
        # Liste todos os campos que você quer que apareçam no formulário
        fields = [
            'titulo', 'descricao', 'data_evento', 'local', 
            'categoria', 'preco_base', 'imagem'
        ]
        
        # Opcional: Customizar classes ou labels
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 4}), # Ajusta o tamanho da área de texto
            # Note: O campo 'imagem' será renderizado corretamente pelo Django/Bootstrap.
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # 🌟 Aplicar a classe 'form-control' do Bootstrap a TODOS os campos
        for field_name, field in self.fields.items():
            if field_name not in ['imagem']: # Campo de imagem não precisa de form-control
                field.widget.attrs['class'] = 'form-control'

IngressoFormSet = inlineformset_factory(
    Evento, 
    Ingresso, 
    fields=('tipo', 'preco', 'quantidade_disponivel'),
    extra=1, # Começa com 1 formulário vazio
    can_delete=True
)