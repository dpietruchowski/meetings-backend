from django.views.generic import View
from django.http import HttpResponse, JsonResponse

import json
import pdb

def dict_object(properties, instance):
    instance_dict = {}
    for prop in properties:
        instance_dict.update({prop: str(getattr(instance, prop))})
    return instance_dict

class BaseView(View):
    model_class = None
    form = []
    def dispatch(self, request, *args, **kwargs):
        self.pk = self.kwargs.get('pk')
        self.object = None
        if (self.pk is not None):
            queryset = self.model_class.objects.filter(pk=self.pk)
            if queryset:
                self.object = queryset[0]
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if (self.object is not None):
            resp = {'ok': True, 'data': self.convert_object()}
        else:
            resp = {'ok': False}
        print(resp)
        return JsonResponse(json.dumps(resp), safe=False)

    def delete(self, request, *args, **kwargs):
        try:
            response = {'ok': True}
            self.object.delete()
        except:
            response = {'ok': False}
        return JsonResponse(json.dumps(response), safe=False)

    def put(self, request, *args, **kwargs):
        if (self.object is not None):
            json_data = json.loads(request.body)
            for f in self.form:
                if f in json_data:
                    setattr(self.object, f, json_data.get(f))

            if self.put_validate():
                self.object.save()
                resp = {'ok': True, 'data': self.convert_object()}
            else:
                resp = {'ok': False}
        else:
            resp = {'ok': False}
        return JsonResponse(json.dumps(resp), safe=False)

    def put_validate(self):
        return True

    def convert_object(self):
        dict_obj = dict_object(self.form, self.object)
        dict_obj.update({'id': self.object.id})
        return dict_obj

class QueryView(View):
    model_class = None
    queries = []
    form = []
    def get(self, request, *args, **kwargs):
        avaiable = True
        for query in self.queries:
            if not query in request.GET:
                avaiable = False
                break
        if avaiable:
            return self.search(request)
        else:
            return self.get_all(request)

    def post(self, request, *args, **kwargs):
        instance = self.model_class()

        json_data = json.loads(request.body)
        for f in self.form:
            if f in json_data:
                setattr(instance, f, json_data.get(f))

        if self.put_validate():
            instance.save()
            resp = {'ok': True, 'data': self.convert_object(instance)}
        else:
            resp = {'ok': False}
        return JsonResponse(json.dumps(resp), safe=False)

    def get_all(self, request):
        model_results = self.model_class.objects.all()
        print(model_results)
        return self.json_response(model_results)

    def json_response(self, model_results):
        results = []
        for obj in model_results:
            results.append(self.convert_object(obj))
        return JsonResponse(json.dumps(results[:10]), safe=False)

    def convert_object(self, obj):
        dict_obj = dict_object(self.form, obj)
        dict_obj.update({'id': obj.id})
        return dict_obj

    def search(self, request):
        pass

    def put_validate(self):
        return True


class NameSearchView(QueryView):
    queries = [u'query']
    model = None
    def search(self, request):
        value = request.GET[u'query']
        model_results = self.model.objects.filter(name__icontains=value)
        return self.json_response(model_results)