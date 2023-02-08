from django.core.paginator import Paginator
from django.db.models import Count, Avg, Q, F
from django.http import JsonResponse, HttpResponse
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from amazing_hunting import settings
from authentication.models import User
from authentication.permissions import VacancyCreatePermission
from vacancies.models import Vacancy, Skill
from vacancies.serializers import VacancyListSerializer, VacancyDetailSerializer, VacancyCreateSerializer, \
    VacancyUpdateSerializer, VacancyDestroySerializer, SkillSerializer


def hello():
    return HttpResponse("Hello World!")


@extend_schema_view(
    list=extend_schema(
        description="Retrieve skill list",
        summary="Skill list",
    ),
    create=extend_schema(
        description="Create new skill",
        summary="Create skill",
    ),
)
class SkillViewSet(ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


class VacancyListView(ListAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyListSerializer

    @extend_schema(
        description="Retrieve vacancy list",
        summary="Vacancy List",
    )
    def get(self, request, *args, **kwargs):
        vacancy_text = request.GET.get("text", None)
        if vacancy_text:
            self.queryset = self.queryset.filter(
                text__icontains=vacancy_text
            )

        skills = request.GET.getlist("skill", None)
        skills_q = None
        for skill in skills:
            if not skills_q:
                skills_q = Q(skills__name__contains=skill)
            else:
                skills_q |= Q(skills__name__contains=skill)
        if skills_q:
            self.queryset = self.queryset.filter(skills_q)

        return super().get(request, *args, **kwargs)


class VacancyDetailView(RetrieveAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyDetailSerializer
    permission_classes = [IsAuthenticated]


class VacancyCreateView(CreateAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyCreateSerializer
    permission_classes = [IsAuthenticated, VacancyCreatePermission]


class VacancyUpdateView(UpdateAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyUpdateSerializer
    http_method_names = ["put"]


class VacancyDeleteView(DestroyAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyDestroySerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_vacancies(request):
    users_qs = User.objects.annotate(vacancies=Count('vacancy'))

    paginator = Paginator(users_qs, settings.TOTAL_ON_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    users = []
    for user in users_qs:
        users.append({
            "id": user.id,
            "name": user.username,
            "vacancies": user.vacancies,
        })

    response = {
        "items": users,
        "avg": users_qs.aggregate(avg=Avg('vacancies'))["avg"],
        "num_pages": page_obj.paginator.num_pages,
        "total": page_obj.paginator.count,
    }

    return JsonResponse(response, safe=False)


class VacancyLikeView(UpdateAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyDetailSerializer
    http_method_names = ["put"]

    @extend_schema(deprecated=True)
    def put(self, request, *args, **kwargs):
        Vacancy.objects.filter(pk__in=request.data).update(likes=F('likes') + 1)

        return JsonResponse(VacancyDetailSerializer(Vacancy.objects.filter(pk__in=request.data), many=True).data,
                            safe=False)
