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
            normal_row='<div class="row mb-3"><label class="col-sm-2 col-form-label">%(label)s</label><div class="col-sm-10">%(field)s<small class="text-danger">%(errors)s</small><small  class="text-info">%(help_text)s</small></div></div>',
            error_row="%s",
            row_ender="</div>",
            help_text_html='<br /><span class="helptext">%s</span>',
            errors_on_separate_row=False,
        )
