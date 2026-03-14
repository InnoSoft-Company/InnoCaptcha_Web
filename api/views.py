from rest_framework.views import APIView
from django.http import HttpResponse
from .models import ReposVisitors

class ReposVisitorsCountShield(APIView):
  def get(self, request, format=None):
    count = ReposVisitors.objects.count()
    label = "visitors"
    w_label = max(50, 8 * len(label) + 20)
    w_value = max(30, 14 + len(str(count)) * 8)
    w_total = w_label + w_value
    h = 20
    svg = f'''
    <svg xmlns="http://www.w3.org/2000/svg" width="{w_total}" height="{h}">
      <linearGradient id="s" x2="0" y2="100%">
        <stop offset="0" stop-color="#fff" stop-opacity=".7"/>
        <stop offset=".1" stop-color="#aaa" stop-opacity=".1"/>
        <stop offset=".9" stop-opacity=".3"/>
        <stop offset="1" stop-opacity=".5"/>
      </linearGradient>
      <mask id="m"><rect width="{w_total}" height="{h}" rx="3" fill="#fff"/></mask>
      <g mask="url(#m)">
        <rect width="{w_label}" height="{h}" fill="#555"/>
        <rect x="{w_label}" width="{w_value}" height="{h}" fill="#007ec6"/>
        <rect width="{w_total}" height="{h}" fill="url(#s)"/>
      </g>
      <g fill="#fff" font-family="Verdana,Geneva,DejaVu Sans,sans-serif" font-size="11">
        <text x="{w_label/2}" y="14" text-anchor="middle">{label}</text>
        <text x="{w_label + w_value/2}" y="14" text-anchor="middle">{count}</text>
      </g>
    </svg>
    '''
    return HttpResponse(svg, content_type="image/svg+xml")

