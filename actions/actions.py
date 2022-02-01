# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List,Union

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
import re
import requests
import json
from rasa_sdk.events import SlotSet
from rasa_sdk.events import AllSlotsReset



class ValidateForm(FormValidationAction):
     

    def name(self) -> Text:
         return "validate_details_form"
         



    def validate_name(
             self,
             value: Text,
             dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any],
         ) -> Dict[Text, Any]:
            
            
            name = tracker.get_slot("name")
            print("name:",name)
            if name is not None:
                return{"name": value}
            else:
                dispatcher.utter_message(response = "utter_wrong_name")
                return{"name":None}

    def validate_address(
             self,
             value: Text,
             dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any],
         ) -> Dict[Text, Any]:
            location = tracker.get_slot("address")
            print("address:",location)
            if location is not None:
                return{"address": value}
            else:
                    dispatcher.utter_message(response = "utter_wrong_location")
                    return{"address":None}

    def validate_phonenumber(
             self,
             value: Text,
             dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any],
         ) -> Dict[Text, Any]:
            
            phonenumber = tracker.get_slot("phonenumber")
            print("phonenumber",phonenumber)
            if len(phonenumber) == 10 and phonenumber.isdigit():
                return{"phonenumber": value}
            else:
                    dispatcher.utter_message(response = "utter_wrong_phonenumber")
                    return{"phonenumber":None}

    def validate_pincode(
             self,
             value: Text,
             dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any],
         ) -> Dict[Text, Any]:
            pincode = tracker.get_slot("pincode")
            print("pincode",pincode)
            if pincode.isdigit() and len(pincode) == 6:
                return{"pincode": value}
            else:
                    dispatcher.utter_message(response = "utter_wrong_pincode")
                    return{"pincode":None}

    def validate_email(
             self,
             value: Text,
             dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any],
         ) -> Dict[Text, Any]:
            email = tracker.get_slot("email")
            print("email",email)
            valid = re.match('([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+',email)
            if valid is not None:
                return{"email": value}
            else:
                dispatcher.utter_message(response = "utter_wrong_email")
                return{"email":None}
class Reset_Slots(Action):
    def name(self):
        return "action_reset_slots"

    def run(self, dispatcher, tracker, domain):
        return [SlotSet("carry_name", None),SlotSet("carry_phonenumber", None)]

class Reset_del_slots(Action):
    def name(self):
        return "action_reset_del_slots"

    def run(self, dispatcher, tracker, domain):
        return [SlotSet("name", None),SlotSet("address", None),SlotSet("phonenumber", None),SlotSet("pincode", None),SlotSet("email", None),]

   
class ValidateCarryForm(FormValidationAction):
     

    def name(self) -> Text:
         return "validate_carry_form"

    def validate_carry_name(
             self,
             value: Text,
             dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any],
         ) -> Dict[Text, Any]:
            
            
            name = tracker.get_slot("carry_name")
            print("carry_name:",name)
            if name is not None:
                return{"carry_name": value}
            else:
                dispatcher.utter_message(response = "utter_wrong_name")
                return{"carry_name":None}

    def validate_carry_phonenumber(
             self,
             value: Text,
             dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any],
         ) -> Dict[Text, Any]:
            
            phonenumber = tracker.get_slot("carry_phonenumber")
            print("carry_phonenumber",phonenumber)
            if len(phonenumber) == 10 and phonenumber.isdigit():
                return{"carry_phonenumber": value}
            else:
                    dispatcher.utter_message(response = "utter_wrong_phonenumber")
                    return{"carry_phonenumber":None}



class ActionResourcesList(Action):

    def name(self) -> Text:
        return "action_resources_list"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            res = {"attachment": {"type": "template", "payload": {
            "template_type": "generic", "elements": []}}}
            sender_id= tracker.sender_id
            print("sender id:",sender_id)
            text = tracker.latest_message.get("text")
            print("last",text)

            loc = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address="+text+"&key=AIzaSyA6gEfQ--K1SIz2Zj8CRzWHUiK68bSEDXY").json()
            for x in loc["results"]:
                print("loc",x["geometry"]["location"]["lat"])
                lat = x["geometry"]["location"]["lat"]
                lng = x["geometry"]["location"]["lng"]
                lat_s = str(lat)
                lng_s = str(lng)
                print("lat =",lat)
                print("lng =",lng)
                print("lat =",lat_s)
                print("lng =",lng_s)
                url = requests.get("https://myeats.cedexdemo.in/api/v1/restaurants?latitude="+lat_s+"&longitude="+lng_s).json()
                c=0
                for x in url["data"]:
                    c = c+1
                    if(c <=10):
                        
                        print("api",x["name"])
                        print("id%d" % x["id"])
                        res["attachment"]["payload"]["elements"].append({
                                "title": x["name"],
                                "subtitle": x["about"],
                                "image_url": x["logo"],
                                "buttons": [{
                                    "title": "View Categories",
                                    "payload": "restaurant_id|%d" % x["id"],
                                    "type": "postback"   
                                
                                }
                                ]
                            })

                
                print("values")
               
                dispatcher.utter_message(json_message=res)
            


class ActionProductList(Action):

    def name(self) -> Text:
        return "action_product_list"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
             res1 = {"attachment": {"type": "template", "payload": {
             "template_type": "generic", "elements": []}}}
             url = requests.get("https://myeats.cedexdemo.in/api/v1/restaurants").json()
             text2 = tracker.latest_message.get("text")
            
             print("lastone",text2)
             new = text2.split("|")[1]
             print(new)
             for x in url["data"]:
                
                 if(text2 == "restaurant_id|%d"%x["id"]):
                    print("success")
                    for y in x["categories"]:
                        print("cat testid",y["id"])
                
                        res1["attachment"]["payload"]["elements"].append({
                        
                                "title": y["name"],
                                
                                "buttons": [{
                                    "title": "View Products",
                                    "payload": "category_id|%d" % y["id"],
                                    "type": "postback"   
                            }
                            ]
                        })
                 
             dispatcher.utter_message(json_message=res1)
             return [SlotSet("restaurant", text2)]
             

class ActionfoodList(Action):

    def name(self) -> Text:
        return "action_food_list"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
             print("inside foods")
             res2 = {"attachment": {"type": "template", "payload": {
             "template_type": "generic", "elements": []}}}
             url = requests.get("https://myeats.cedexdemo.in/api/v1/restaurants").json()
             text3 = tracker.latest_message.get("text")
             rest_slot = tracker.get_slot("restaurant")
             print("rest_slot",rest_slot)
             print("asda",text3)
             new = text3.split("|")[1]
             print(new)
             for x in url["data"]:
                 if(rest_slot == "restaurant_id|%d"%x["id"]):
                    item = x["categories"]
                    #print("id's",item["id"])
                    #for y in x["categories"]:
                    for y in item:
                        print("testid",y["id"])
                        #if(text3 == "category_id|%d"% y["id"]):
                        if(text3 == "category_id|%d"%y["id"]):
                            print("successwwwww")
                            
                            for z in y["products"]:
                                if(z["is_available"] == 1):
                   
                                    res2["attachment"]["payload"]["elements"].append({
                                
                                        "title": z["name"],
                                        "subtitle": z["price"],
                                        "image_url": z["image"],
                                        "buttons": [{
                                            "title": "Add to Cart",
                                            "payload": "product_id|%d" % z["id"],
                                            "type": "postback"   
                                    }
                                    ]
                                })
                        
                 
             dispatcher.utter_message(json_message=res2)
             return [SlotSet("foods", text3)]

class ActionQuantityList(Action):

    def name(self) -> Text:
        return "action_quantity_list"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

                        product_id = tracker.latest_message.get("text")
                        new = product_id.split("|")[1]
                        print("prod =",new)
                        dispatcher.utter_message(response ="utter_quantity")
                        return [SlotSet("prod_id", new)]
            
             

class ActionCartList(Action):

    def name(self) -> Text:
        return "action_cart_list"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
  
                        url = requests.get("https://myeats.cedexdemo.in/api/v1/restaurants").json()
                        quan = tracker.latest_message.get("text")
                        print("quantity",quan)
                        cartid = tracker.get_slot("cart")
                        new = tracker.get_slot("prod_id")
                        rest_id = tracker.get_slot("restaurant")
                        cat_id = tracker.get_slot("foods")
                      
                        print("product_id",new)
                        new2 = rest_id.split("|")[1]
                        print(new2)
                        
                        print("cart",new)
                        print("cart",cartid)

                        res4 = {"attachment": {"type": "template", "payload": {
                        "template_type": "generic", "elements": []}}}
                        print("bef")
                        payload={'latitude': '76.2992273',
                                                'longitude': '9.9995091',
                                                'product_id': new,
                                                'quantity': quan}
                        print(payload)
                        if cartid is None:
                            print("asdfr")
                            #create = requests.get("https://myeats.cedexdemo.in/api/v1/carts").json()
                            create = "https://myeats.cedexdemo.in/api/v1/carts"
                            payload={'latitude': '76.2992273',
                                                'longitude': '9.9995091',
                                                'product_id':  new,
                                                'quantity': quan}
                            files=[

                                                ]
                            headers = {
                                                'Accept': 'application/json'
                                                }
                            response = requests.request("POST", create, headers=headers, data=payload, files=files)
                            item = response.json()
                           
                            #print(response.json())
                            id = item["data"]["cart"]
                            print("id",id["id"])
                            new_id = id["id"]
                            for x in url["data"]:
                                if(rest_id == "restaurant_id|%d"%x["id"]):
                                    for y in x["categories"]:
                                        if(cat_id == "category_id|%d"%y["id"]):
                                            for z in y["products"]:
                                                print(z["id"])
                                                print("product_id|"+new) 
                                                if("product_id|"+new == "product_id|%d"%z["id"]):
                                                    print("successwwwww")
                                  
                                                    res4["attachment"]["payload"]["elements"].append({
                                                    
                                                            "title": z["name"],
                                                            "subtitle": z["price"],
                                                            "image_url": z["image"],
                                                            "buttons": [{
                                                                "title": "Checkout",
                                                                "payload": "check",
                                                                "type": "postback"   
                                                            },
                                                            {
                                                                "title":"Add More Products",
                                                                "payload": cat_id,
                                                                "type":"postback"    
                                                            }
                                                        ]
                                                    })
                                            break
                                
                            dispatcher.utter_message(json_message=res4)
                            return[SlotSet("cart",new_id)]
               
                           
                        else:
                        #print("Data =",cartdata)
                                text4 = tracker.get_slot("cart")
                                print("cart",text4)
                                print("else")
                                payload={'product_id': new,
                                'quantity': '1'}
                                print("dybanmic",payload)
                                add = "https://myeats.cedexdemo.in/api/v1/carts/" + text4
                                
                                files=[

                                ]
                                headers = {
                                'Accept': 'application/json',
                            
                                }

                                response = requests.request("POST", add, headers=headers, data=payload, files=files)
                                print("res",response)
                                dat = response.json()
                                #print("items",items)
                                items = dat["data"]["cart"]["items"]
                                #print("items",items)
                                for x in items:                                     
                                    res4["attachment"]["payload"]["elements"].append({
                                                        
                                        "title": x["name"],
                                        "subtitle": x["price"],
                                        "image_url": x["image"],
                                        "buttons": [{
                                            "title": "Checkout",
                                            "payload": "check",
                                            "type": "postback"   
                                        },
                                        {
                                            "title":"Add More Products",
                                            "payload": cat_id,
                                            "type":"postback"    
                                                                }
                                                            ]
                                                        })
                                       
                        dispatcher.utter_message(json_message=res4)

class ActionReceiptList(Action):

    def name(self) -> Text:
        return "action_receipt_list"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

                        
                        text5 = tracker.get_slot("cart")
                        text6 = str(text5)
                        name = tracker.get_slot("name")
                        print("rec_cart",text5)
                        url = requests.get("https://myeats.cedexdemo.in/api/v1/carts/"+ text6).json()
                        rec = url["data"]["items"]
                    

                        res5 = {
                                "attachment":{
                                "type":"template",
                                "payload":{
                                    "template_type":"receipt",
                                    "recipient_name":"jogey",
                                    "order_number":"12345678902",
                                    "currency":"USD",
                                    "payment_method":"Visa 2345",        
                                    "order_url":"http://originalcoastclothing.com/order?order_id=123456",
                                    "timestamp":"1428444852",         
                                    "address":{
                                    "street_1":"1 Hacker Way",
                                    "street_2":"",
                                    "city":"Menlo Park",
                                    "postal_code":"94025",
                                    "state":"CA",
                                    "country":"US"
                                    },
                                    "summary":{
                                    "subtotal":75.00,
                                    "shipping_cost":4.95,
                                    "total_tax":6.19,
                                    "total_cost":56.14
                                    },
                                    "adjustments":[
                                    {
                                        "name":"New Customer Discount",
                                        "amount":20
                                    },
                                    {
                                        "name":"$10 Off Coupon",
                                        "amount":10
                                    }
                                    ],
                                    "elements":[]
                               

                                }
                                }
                               

                                
                            }
                        for x in rec:
                            res5["attachment"]["payload"]["elements"].append({
                                        "title":x["name"],
                                        "subtitle":x["price"],
                                        "quantity":x["quantity"],
                                        "price":x["price"],
                                        "currency":"INR",
                                        "image_url":x["image"]
                                })


                        dispatcher.utter_message(json_message=res5)            