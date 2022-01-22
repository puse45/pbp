from base.forms import BaseModelForm
from travel.models import Permit


class PermitForm(BaseModelForm):
    class Meta:
        model = Permit
        fields = (
            "date_of_travel",
            "date_of_return",
            "country_of_origin",
            "country_of_destination",
            "age_of_traveller",
            "is_supervised",
        )

    def as_plain(self):
        "Returns this form rendered as HTML <tr>s -- excluding the <table></table>."
        return self._html_output(
            normal_row='<div class="col-lg-3 col-md-3 col-sm-4 form-control-label">%(label)s</div> <div class="col-lg-9 col-md-9 col-sm-8"><div class="form-group">%(field)s%(errors)s%(help_text)s</div></div>',
            error_row="%s",
            row_ender="</div>",
            help_text_html='<br /><span class="helptext">%s</span>',
            errors_on_separate_row=False,
        )
