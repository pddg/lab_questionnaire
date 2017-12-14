import io
from datetime import datetime
import pandas as pd
from django.views.generic import TemplateView, UpdateView, ListView, FormView, CreateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse
from django.http import Http404
from .models import StudyOffice
from accounts.models import MyUser


class TopPageView(ListView):
    template_name = "questionnaire/top_page_labo.html"
    model = StudyOffice


class TopPageStudentsView(ListView):
    template_name = "questionnaire/top_page_students.html"
    model = MyUser


class EditProfileView(UpdateView):
    template_name = "questionnaire/edit_profile.html"
    fields = ("display_name", "first_choice")

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('top_page')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EditProfileView, self).dispatch(*args, **kwargs)


class ResultDownloadView(TemplateView):
    def render_to_response(self, context):
        from accounts.models import MyUser

        output_type = context["type"]
        output_param = "application/force-download"
        name = "lab_questionnaire_result" + "_" + datetime.now().strftime('%Y%m%d_%H%M%S') + "." + output_type

        # ユーザデータのテーブルを作る（詳細データ）
        user_table_header = [
            u"学生ID",
            u"表示名",
            u"研究室番号",
            u"研究室名",
            u"希望者数",
            u"定員",
            u"ステータス",
        ]
        user_table_data = []
        for user in MyUser.objects.all():
            if user.is_active:
                user_table_data.append([
                    user.student_number,
                    user.display_name if user.display_name is not None else "-",
                    user.first_choice.number if user.first_choice is not None else "-",
                    user.first_choice.name if user.first_choice is not None else "-",
                    user.first_choice.first_choiced_user.count() if user.first_choice is not None else "-",
                    user.first_choice.capacity if user.first_choice is not None else "-",
                    "作成者" if user.is_superuser else "管理者" if user.is_staff else "-",
                ])
        user_table = pd.DataFrame(data=user_table_data, columns=user_table_header)
        user_table = user_table.sort_values(by=[u"研究室番号", u"学生ID"], ascending=True)

        # 研究室データのテーブルを作る（統計データ）
        study_office_table_header = [
            u"研究室番号",
            u"研究室名",
            u"希望者数",
            u"定員",
        ]
        study_office_table_data = []
        for study_office in StudyOffice.objects.all():
            study_office_table_data.append([
                study_office.number,
                study_office.name,
                study_office.first_choiced_user.count(),
                study_office.capacity,
            ])
        study_office_table = pd.DataFrame(data=study_office_table_data, columns=study_office_table_header)
        study_office_table.sort_values(by=[u"研究室番号"], ascending=True)

        if output_type == "xlsx":
            with io.BytesIO() as buf:
                with pd.ExcelWriter(buf, engine='xlsxwriter') as writer:
                    user_table.to_excel(writer, sheet_name='学生データ', index=False)
                    study_office_table.to_excel(writer, sheet_name='研究室データ', index=False)
                    writer.save()
                response = HttpResponse(
                    buf.getvalue(),
                    content_type=output_param
                )
        elif output_type == "csv":
            with io.StringIO() as buf:
                user_table.to_csv(buf, index=False, encoding="utf-8")
                response = HttpResponse(
                    buf.getvalue(),
                    content_type=output_param
                )
        else:
            raise Http404

        response['Content-Disposition'] = 'filename="{}"'.format(name)
        return response

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ResultDownloadView, self).dispatch(*args, **kwargs)
