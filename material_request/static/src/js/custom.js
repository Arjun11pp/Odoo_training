/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from '@web/core/network/rpc';
publicWidget.registry.MaterialRequest = publicWidget.Widget.extend({
   selector: "#wrap",
   events: {
       'change .operation': '_onChangeType',
       'click .add_total_project': '_onClickAddMaterial',
       'click .remove_line': '_onClickRemoveLine',
       'click .custom_create': '_onClickSubmit',
   },
   _onClickSubmit: async function (ev) {
       ev.preventDefault();
       var name = $('#name').val();
       if(!name){
           alert('please enter the name')
           return;}
       var date = $('#date').val();
       if(!date){
           alert('please choose a  date')
           return;}
       var material_order_ids = [];
       var isError=false
       var isQuantity=false
       $('#material_table tbody tr.material_order_line').each(function () {
           let product = $(this).find('select[name="product"]').val();
           let quantity = $(this).find('input[name="quantity"]').val();
           let operation = $(this).find('select[name="operation"]').val();
           let source = $(this).find('select[name="source"]').val();
           let destination = $(this).find('select[name="destination"]').val();
           if (operation === 'internal' && (!source || !destination)){
           isError =true
           return ;
           }
           if (quantity <= 0)
            {
            isQuantity=true
            }
           material_order_ids.push({
               'product_id': product,
               'quantity': quantity,
               'request_type': operation,
               'source_location_id': source || null,
               'destination_location_id': destination || null
           });
       });
        if(isError){
        alert('please fill source and destination')
        return;}
        if(isQuantity){
        alert('please enter a positive quantity')
        return;}
       try {
           let response = await rpc('/material/submit', {
               req_name: name,
               date: date,
               request_line_ids: material_order_ids
           });
           console.log('Response:', response);
           alert('Material request submitted successfully!');
            window.location.reload(true);
       } catch (error) {
           console.error('Error:', error);
           alert('Enter the fields ');
       }
},

   _onClickAddMaterial: function (ev) {
       var $new_row = $('#material_table tbody tr.material_order_line:first').clone();
       $new_row.find('input, select').val('');
       $new_row.appendTo('#material_table tbody');
   },
   _onClickRemoveLine: function (ev) {
       if ($('#material_table tbody tr').length > 1) {
           $(ev.target).closest('tr').remove();
       } else {
           alert("You must have at least one material entry.");
       }
   },
   _onChangeType: function (ev) {
       var $row = $(ev.target).closest('tr');
       if ($row.find('.operation').val() === "po") {

           $row.find('select[name="source"]').prop('disabled', true);
           $row.find('select[name="destination"]').prop('disabled', true);
       } else {
           $row.find('select[name="source"]').prop('disabled', false);
           $row.find('select[name="destination"]').prop('disabled', false);
       }
   }
});

