$(document).foundation();


this.ckan.module('slug-generator', function (jQuery, _) {
    return {
        options: {
            prefix: '',
            placeholder: '<slug>',
            i18n: {
                url: _('URL'),
                edit: _('Edit')
            }
        },

        initialize: function () {
            var sandbox = this.sandbox;
            var options = this.options;
            var el = this.el;
            var _ = sandbox.translate;

            var slug = el.slug();
            var parent = slug.parents('.control-group');

            if (!(parent.length)) {
                return;
            }

            // Leave the slug field visible
            if (!parent.hasClass('error')) {
                // Horrible hack to make sure that IE7 rerenders the subsequent
                // DOM children correctly now that we've render the slug preview element
                // We should drop this horrible hack ASAP
                if (jQuery('html').hasClass('ie7')) {
                    jQuery('.btn').on('click', preview, function () {
                        jQuery('.controls').ie7redraw();
                    });
                    preview.hide();
                    setTimeout(function () {
                        preview.show();
                        jQuery('.controls').ie7redraw();
                    }, 10);
                }
            }

            // Watch for updates to the target field and update the hidden slug field
            // triggering the "change" event manually.
            sandbox.subscribe('slug-target-changed', function (value) {
                slug.val(value).trigger('change');
            });
        }
    };
});


this.ckan.module('department-target', function (jQuery, _) {
    return {
        initialize: function () {
            var sandbox = this.sandbox;
            var el = this.el;

            if (el.val() != '') {
                sandbox.publish('department-target-changed', el.find(':selected'));
            }

            el.on('change.department-target', function () {
                sandbox.publish('department-target-changed', el.find(':selected'));
            });

        }
    };
});


this.ckan.module('department-generator', function (jQuery, _) {
    return {
        initialize: function () {
            var sandbox = this.sandbox;
            var el = this.el;

            sandbox.subscribe('department-target-changed', function (selected) {
                var org = selected.text();
                var dept = el.data('selected');
                var choices = el.data('choices')[org];

                el.find('option').remove().end().append('<option value=""></option>');

                if (choices) {
                    for (var i = 0; i < choices.length; i++) {
                        var sel = (dept == choices[i] ? ' selected="true"' : '');
                        el.append('<option value="' + choices[i] + '"' + sel + '>' + choices[i] + '</option>');
                    }
                } else {
                    console.log('no departemnts found for this org');
                }

            });

        }
    };
});

this.ckan.module('terms-reveal', function (jQuery) {
    return {
        initialize: function () {
            console.log("test");
            jQuery('#terms-reveal').foundation('open');
            came_from_val = jQuery("#terms-came-from");
            console.log(came_from_val);
            jQuery('#terms-submit').on('click', function(){
                document.cookie ='wprdc_user_terms=1337';
                // jQuery.post('terms-of-service', {'came_from': came_from_val});
                jQuery('#terms-reveal').foundation('close');
            })
        }
    }
});