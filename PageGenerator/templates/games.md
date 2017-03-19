# {{ update_time }}

{% for domain in domains %}
* [{{ domain.name }}](#{{ domain.name | lower }})
{% endfor %}

{% for domain in domains %}

## {{ domain.name }}

| Preview                                                         | Name                                                          | Platform           | PsPlus Price             | Origin Price            | Discount                           |
| :-------------------------------------------------------------: | :-----------------------------------------------------------: | :----------------: | :----------------------: | :---------------------: | :--------------------------------: |
{% for game in domain.games %}
{% if game.discount > 0 %}
| ![{{ game.game_name }}]({{ game.image_url | markdown_escape }}) | [{{ game.game_name }}]({{ game.game_url | markdown_escape }}) | {{ game.platform}} | {{ game.ps_plus_price }} | {{ game.origin_price }} | {{ (game.discount * 100) | int }}% |
{% endif %}
{% endfor %}
{% endfor %}
