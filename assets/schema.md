# Database Schema for atithi

### TechStack - Firebase Realtime Database | MindMeld API | Flask

* user
  * {phone number/ webhook_id}
    * status - (idle or travelling)
    * location
      * source (only 1)
      * current (only 1)
      * destinations (may be multiple)
    * preferences
      * food - veg/non-veg/cuisines
      * transport - public/gov/rental
      * Hotels - stars


  