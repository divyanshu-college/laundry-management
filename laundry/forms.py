from django import forms
from .models import LaundryBooking, LaundryItem


class LaundryBookingForm(forms.ModelForm):

    bedsheet = forms.IntegerField(min_value=0, max_value=7, initial=0, required=False)
    pillow_cover = forms.IntegerField(min_value=0, max_value=7, initial=0, required=False)
    towel = forms.IntegerField(min_value=0, max_value=7, initial=0, required=False)
    ac_towel = forms.IntegerField(min_value=0, max_value=7, initial=0, required=False)
    salwar = forms.IntegerField(min_value=0, max_value=7, initial=0, required=False)
    kurta = forms.IntegerField(min_value=0, max_value=7, initial=0, required=False)
    lower_pajama = forms.IntegerField(min_value=0, max_value=7, initial=0, required=False)
    jacket = forms.IntegerField(min_value=0, max_value=7, initial=0, required=False)
    sneakers = forms.IntegerField(min_value=0, max_value=7, initial=0, required=False)
    jeans = forms.IntegerField(min_value=0, max_value=7, initial=0, required=False)
    tshirt = forms.IntegerField(min_value=0, max_value=7, initial=0, required=False)
    school_university_pant = forms.IntegerField(min_value=0, max_value=7, initial=0, required=False)
    school_university_shirt = forms.IntegerField(min_value=0, max_value=7, initial=0, required=False)
    civil_pant = forms.IntegerField(min_value=0, max_value=7, initial=0, required=False)
    civil_shirt = forms.IntegerField(min_value=0, max_value=7, initial=0, required=False)
    school_sweater = forms.IntegerField(min_value=0, max_value=7, initial=0, required=False)
    school_coat = forms.IntegerField(min_value=0, max_value=7, initial=0, required=False)
    skirt = forms.IntegerField(min_value=0, max_value=7, initial=0, required=False)
    dupatta = forms.IntegerField(min_value=0, max_value=7, initial=0, required=False)
    turban = forms.IntegerField(min_value=0, max_value=7, initial=0, required=False)
    apron = forms.IntegerField(min_value=0, max_value=7, initial=0, required=False)
    white_coat = forms.IntegerField(min_value=0, max_value=7, initial=0, required=False)
    upper_hoodie = forms.IntegerField(min_value=0, max_value=7, initial=0, required=False)
    small_blanket = forms.IntegerField(min_value=0, max_value=7, initial=0, required=False)
    big_blanket = forms.IntegerField(min_value=0, max_value=7, initial=0, required=False)

    class Meta:
        model = LaundryBooking
        fields = ['student']

    def clean(self):

        cleaned_data = super().clean()

        total = 0

        for item_type in LaundryItem.ITEM_CHOICES:
            field_name = item_type[0]
            quantity = cleaned_data.get(field_name) or 0
            total += quantity

        if total < 1:
            raise forms.ValidationError(
                "Please select at least one clothes item."
            )

        if total > 7:
            raise forms.ValidationError(
                "Maximum 7 clothes are allowed in one booking."
            )

        cleaned_data['total_clothes'] = total

        return cleaned_data

    def save(self, commit=True):

        booking = super().save(commit=False)

        total = self.cleaned_data['total_clothes']

        booking.total_clothes = total

        if commit:
            booking.save()

            for item_type in LaundryItem.ITEM_CHOICES:

                field_name = item_type[0]
                quantity = self.cleaned_data.get(field_name) or 0

                if quantity > 0:
                    LaundryItem.objects.create(
                        booking=booking,
                        item_type=field_name,
                        quantity=quantity
                    )

        return booking