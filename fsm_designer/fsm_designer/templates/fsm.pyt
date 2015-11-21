

@singleton
class {{state}}(State):
    {%for f_name, transitions in functions %}{%for t in transitions%}
    @transition('{{t.to_state}}'){%endfor%}
    def {{f_name}}(self, controller):
        {%for t in transitions-%}
        controller.changeState({{t.to_state}})
        {%endfor%}{%else%}pass
    {%endfor%}

