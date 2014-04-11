import sys
from .compat import *
from .fieldmaps import FieldMap, IntegerFieldMap, DateTimeFieldMap, TermsListFieldMap
from wordpress_xmlrpc.exceptions import FieldConversionError


class WordPressBase(object):
    """
    Base class for representing a WordPress object. Handles conversion
    of an XML-RPC response to an object, and construction of a `struct`
    to use in XML-RPC requests.

    Child classes should define a `definition` property that contains
    the list of fields and a `FieldMap` instance to handle conversion
    for XML-RPC calls.
    """
    definition = {}

    def __init__(self, xmlrpc=None):
        # create private variable containing all FieldMaps for the `definition`
        self._def = {}

        for key, value in self.definition.items():
            # if the definition was not a FieldMap, create a simple FieldMap
            if isinstance(value, FieldMap):
                self._def[key] = value
            else:
                self._def[key] = FieldMap(value)

            # convert and store the value on this instance if non-empty
            try:
                converted_value = self._def[key].convert_to_python(xmlrpc)
            except Exception:
                e = sys.exc_info()[1]
                raise FieldConversionError(key, e)
            if converted_value is not None:
                setattr(self, key, converted_value)

    @property
    def struct(self):
        """
        XML-RPC-friendly representation of the current object state
        """
        data = {}
        for var, fmap in self._def.items():
            if hasattr(self, var):
                data.update(fmap.get_outputs(getattr(self, var)))
        return data

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, unicode(self).encode('utf-8'))


class WordPressTaxonomy(WordPressBase):
    definition = {
        'cap': 'cap',
        'hierarchical': 'hierarchical',
        'is_builtin': '_builtin',
        'label': 'label',
        'labels': 'labels',
        'name': FieldMap('name', default=''),
        'object_type': 'object_type',
        'public': 'public',
        'show_ui': 'show_ui',
    }

    def __unicode__(self):
        if hasattr(self, 'name'):
            return self.name
        return unicode('')


class WordPressTerm(WordPressBase):
    definition = {
        'id': 'term_id',
        'count': IntegerFieldMap('count'),
        'description': 'description',
        'group': 'term_group',
        'name': FieldMap('name', default=''),
        'parent': 'parent',
        'slug': 'slug',
        'taxonomy': 'taxonomy',
        'taxonomy_id': 'term_taxonomy_id',
    }

    def __unicode__(self):
        if hasattr(self, 'name'):
            return self.name
        return unicode('')


class WordPressPost(WordPressBase):
    definition = {
        'comment_status': 'comment_status',
        'content': 'post_content',
        'custom_fields': 'custom_fields',
        'date': DateTimeFieldMap('post_date_gmt'),
        'date_modified': DateTimeFieldMap('post_modified_gmt'),
        'enclosure': 'enclosure',
        'excerpt': 'post_excerpt',
        'guid': 'guid',
        'id': 'post_id',
        'link': 'link',
        'menu_order': IntegerFieldMap('menu_order'),
        'mime_type': 'post_mime_type',
        'parent_id': 'post_parent',
        'password': 'post_password',
        'ping_status': 'comment_status',
        'post_format': 'post_format',
        'post_status': 'post_status',
        'post_type': FieldMap('post_type', default='post'),
        'slug': 'post_name',
        'sticky': 'sticky',
        'terms': TermsListFieldMap(WordPressTerm, 'terms'),
        'terms_names': 'terms_names',
        'thumbnail': 'post_thumbnail',
        'title': FieldMap('post_title', default='Untitled'),
        'user': 'post_author',
    }

    def __unicode__(self):
        if hasattr(self, 'title'):
            return self.title
        return unicode('')


class WordPressPage(WordPressPost):
    definition = dict(WordPressPost.definition, **{
        'template': 'wp_page_template',
        'post_type': FieldMap('post_type', default='page'),
    })


class WordPressComment(WordPressBase):
    definition = {
        'id': 'comment_id',
        'author': 'author',
        'author_email': 'author_email',
        'author_ip': 'author_ip',
        'author_url': 'author_url',
        'content': FieldMap('content', default=''),
        'date_created': DateTimeFieldMap('date_created_gmt'),
        'link': 'link',
        'parent': 'comment_parent',
        'post': 'post_id',
        'post_title': 'post_title',
        'status': 'status',
        'user': 'user_id',
    }

    def __unicode__(self):
        if hasattr(self, 'content'):
            return self.content
        return unicode('')


class WordPressBlog(WordPressBase):
    definition = {
        'id': 'blogid',
        'is_admin': FieldMap('isAdmin', default=False),
        'name': FieldMap('blogName', default=''),
        'url': 'url',
        'xmlrpc': 'xmlrpc',
    }

    def __unicode__(self):
        if hasattr(self, 'name'):
            return self.name
        return unicode('')


class WordPressAuthor(WordPressBase):
    definition = {
        'id': 'user_id',
        'display_name': FieldMap('display_name', default=''),
        'user_login': 'user_login',
    }

    def __unicode__(self):
        if hasattr(self, 'display_name'):
            return self.display_name
        return unicode('')


class WordPressUser(WordPressBase):
    definition = {
        'id': 'user_id',
        'bio': 'bio',
        'display_name': 'display_name',
        'email': 'email',
        'first_name': 'first_name',
        'last_name': 'last_name',
        'nicename': 'nicename',
        'nickname': 'nickname',
        'registered': DateTimeFieldMap('registered'),
        'roles': 'roles',
        'url': 'url',
        'username': 'username',
    }

    def __unicode__(self):
        if hasattr(self, 'nickname'):
            return self.nickname
        return unicode('')


class WordPressMedia(WordPressBase):
    definition = {
        'id': 'attachment_id',
        'caption': 'caption',
        'date_created': DateTimeFieldMap('date_created_gmt'),
        'description': 'description',
        'link': 'link',
        'metadata': 'metadata',
        'parent': 'parent',
        'thumbnail': 'thumbnail',
        'title': FieldMap('title', default=''),
    }

    def __unicode__(self):
        if hasattr(self, 'title'):
            return self.title
        return unicode('')


class WordPressOption(WordPressBase):
    definition = {
        'name': FieldMap('name', default=''),
        'description': 'desc',
        'read_only': FieldMap('readonly', default=False),
        'value': FieldMap('value', default=''),
    }

    def __unicode__(self):
        if hasattr(self, 'name') and hasattr(self, 'value'):
            return '%s="%s"' % (self.name, self.value)
        return unicode('')


class WordPressPostType(WordPressBase):
    definition = {
        'cap': 'cap',
        'hierarchical': 'hierarchical',
        'is_builtin': '_builtin',
        'label': FieldMap('label', default=''),
        'labels': 'labels',
        'map_meta_cap': 'map_meta_cap',
        'menu_icon': 'menu_icon',
        'menu_position': 'menu_position',
        'name': 'name',
        'public': 'public',
        'show_in_menu': 'show_in_menu',
        'supports': 'supports',
        'taxonomies': 'taxonomies',
    }

    def __unicode__(self):
        if hasattr(self, 'name'):
            return self.name
        return unicode('')
