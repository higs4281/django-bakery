"""
Views that inherit from Django's class-based generic views
and add methods that make it convenient for building out 
flat files.
"""
import os
import logging
from django.conf import settings
from django.test.client import RequestFactory
from django.views.generic import TemplateView, DetailView, ListView

logger = logging.getLogger(__name__)


class BuildableTemplateView(TemplateView):

    def build_object(self, url):
        """
        Bake a template page as a flat HTML file.
        You need to pass it the relative URL in.
        """
        logger.debug("Building %s" % url)
        # Make a fake request
        self.request = RequestFactory().get(url)
        # Render the detail page HTML
        html = self.get(self.request).render().content
        # Create the path to save the flat file
        path = os.path.join(settings.BUILD_DIR, url[1:])
        os.path.exists(path) or os.makedirs(path)
        path = os.path.join(path, 'index.html')
        # Write out the data
        outfile = open(path, 'w')
        outfile.write(html)
        outfile.close()


class BuildableListView(ListView):
    """
    A list of all tables.
    """
    build_path = 'index.html'
    
    def build_queryset(self):
        """
        Build the view as a flat HTML file.
        
        Example usage:
            
            TableListView().build_queryset()
        
        """
        # Make a fake request
        self.request = RequestFactory().get(self.build_path)
        # Render the list page as HTML
        html = self.get(self.request).render().content
        # Write it out to the appointed flat file
        path = os.path.join(settings.BUILD_DIR, self.build_path)
        outfile = open(path, 'w')
        outfile.write(html)
        outfile.close()


class BuildableDetailView(DetailView):

    def build_object(self, obj):
        """
        Bake a detail page as a flat HTML file.
        Accepts a BuildableModel, but anything
        with a slug, get_absolute_url and a build
        method will work.
        """
        logger.debug("Building %s" % obj)
        # Make a fake request
        self.request = RequestFactory().get(obj.get_absolute_url())
        # Set the kwargs to fetch this particular object
        self.kwargs = dict(slug=obj.slug)
        # Render the detail page HTML
        html = self.get(self.request).render().content
        # Create the path to save the flat file
        path = os.path.join(settings.BUILD_DIR, obj.get_absolute_url()[1:])
        os.path.exists(path) or os.makedirs(path)
        path = os.path.join(path, 'index.html')
        # Write out the data
        outfile = open(path, 'w')
        outfile.write(html)
        outfile.close()

    def build_queryset(self):
        [self.build_object(o) for o in self.queryset.all()]
