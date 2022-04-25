'''
    Provides the templates for the tooltips.
'''

def percrent(n1):
    return n1

def sankey_hover_template_node():
    '''
        Sets the template for the hover tooltips on the neighborhoods.
        The label is simply the name of the neighborhood in font 'Oswald'.
        Returns:
            The hover template.
    '''
    # TODO : Generate the hover template
    hovertemp = '%{label} a %{value} évènements (%{customdata:.2f}%)<extra></extra>'
    #hovertemp = '<span style="  font-family: Oswald"></span>   %{hovertext}<extra></extra>'
    return hovertemp

def sankey_hover_template_link():
    '''
        Sets the template for the hover tooltips on the neighborhoods.
        The label is simply the name of the neighborhood in font 'Oswald'.
        Returns:
            The hover template.
    '''
    # TODO : Generate the hover template
    hovertemp = '%{source.label} et %{target.label} : %{value} </br><br>Pourcentage pour %{source.label} : %{customdata[0]:.2f}% <br>Pourcentage pour %{target.label} : %{customdata[1]:.2f}%</br></br><extra></extra>'
    #hovertemp = '<span style="  font-family: Oswald"></span>   %{hovertext}<extra></extra>'
    return hovertemp


def barchart_gratuit():
    # 2D9A0F
    hovertemp = '<b style="color: white"> Région</b><span style="color: white"> : %{x} </span><br>'
    hovertemp+="<b style='color: white'>Nombre d'événenemnts</b> <span style='color:white'> : %{y} </span><extra></extra>"
    return hovertemp



def barchart_payant():
    hovertemp = '<b style="color: white"> Catégorie</b><span style="color: white"> : %{x} </span><br>'

    hovertemp += "<b style='color: white'>Nombre d'événenemnts</b> <span style='color: white'> : %{y} </span><extra></extra>"
    return hovertemp
