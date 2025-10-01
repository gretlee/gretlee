import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

// Translation resources
const resources = {
  en: {
    translation: {
      // Login translations
      login: {
        title: 'Disaster Relief Login',
        subtitle: 'Emergency Resource Allocation System',
        username: 'Username',
        usernamePlaceholder: 'Enter your username',
        role: 'Role',
        reliefWorker: 'Relief Worker',
        admin: 'Administrator',
        loginButton: 'Login',
        enterUsername: 'Please enter a username',
        roleInfo: 'Role Information',
        reliefWorkerDesc: 'Can submit and view disaster reports',
        adminDesc: 'Full access - manage centers, run optimization, view predictions'
      },
      
      // Report form translations
      report: {
        title: 'Report Disaster',
        description: 'Click on the map to select a location, then fill in the details',
        latitude: 'Latitude',
        longitude: 'Longitude',
        clickMap: 'Click on map to select',
        people: 'Number of People Affected',
        peoplePlaceholder: 'Enter number of people',
        needType: 'Resource Needed',
        water: 'Water',
        food: 'Food',
        tent: 'Tents/Shelter',
        medical: 'Medical Supplies',
        shelter: 'Temporary Shelter',
        urgency: 'Urgency Level',
        low: 'Low',
        medium: 'Medium',
        high: 'High',
        submit: 'Submit Report',
        submitting: 'Submitting...',
        selectLocation: 'Please select a location on the map',
        success: 'Report submitted successfully! Request ID: {{id}}',
        error: 'Error submitting report: {{error}}',
        networkError: 'Network error. Please check your connection.'
      },
      
      // Map view translations
      map: {
        loading: 'Loading map...',
        legend: 'Map Legend',
        requests: 'Disaster Requests',
        centers: 'Relief Centers',
        allocated: 'Allocated Requests',
        allocationRoutes: 'Allocation Routes',
        optimize: 'Run Optimization',
        adminOnly: 'Only administrators can run optimization',
        optimizeSuccess: 'Optimization completed! {{count}} requests allocated.',
        optimizeError: 'Error running optimization: {{error}}',
        statistics: 'Statistics',
        totalRequests: 'Total Requests',
        pendingRequests: 'Pending Requests',
        allocatedRequests: 'Allocated Requests',
        reliefCenters: 'Relief Centers',
        request: 'Request',
        people: 'People',
        needType: 'Need Type',
        urgency: 'Urgency',
        status: 'Status',
        allocatedTo: 'Allocated To',
        resourcesSent: 'Resources Sent',
        distance: 'Distance',
        center: 'Center',
        water: 'Water Stock',
        food: 'Food Stock',
        tents: 'Tent Stock',
        selectedLocation: 'Selected Location',
        lat: 'Latitude',
        lon: 'Longitude'
      },
      
      // Navigation
      nav: {
        home: 'Home',
        reports: 'Reports',
        map: 'Map',
        analytics: 'Analytics',
        logout: 'Logout',
        language: 'Language'
      }
    }
  },
  
  ur: { // Urdu translations
    translation: {
      login: {
        title: 'آفات سے نجات - لاگ ان',
        subtitle: 'ایمرجنسی وسائل کی تقسیم کا نظام',
        username: 'صارف کا نام',
        usernamePlaceholder: 'اپنا صارف نام درج کریں',
        role: 'کردار',
        reliefWorker: 'امدادی کارکن',
        admin: 'منتظم',
        loginButton: 'لاگ ان کریں',
        enterUsername: 'براہ کرم صارف نام درج کریں',
        roleInfo: 'کردار کی معلومات',
        reliefWorkerDesc: 'آفات کی رپورٹیں جمع کروا اور دیکھ سکتے ہیں',
        adminDesc: 'مکمل رسائی - مراکز کا انتظام، بہتری چلائیں، پیشین گوئیاں دیکھیں'
      },
      
      report: {
        title: 'آفت کی اطلاع دیں',
        description: 'نقشے پر مقام منتخب کرنے کے لیے کلک کریں، پھر تفصیلات بھریں',
        latitude: 'عرض البلد',
        longitude: 'طول البلد',
        clickMap: 'منتخب کرنے کے لیے نقشے پر کلک کریں',
        people: 'متاثرہ افراد کی تعداد',
        peoplePlaceholder: 'افراد کی تعداد درج کریں',
        needType: 'ضروری وسائل',
        water: 'پانی',
        food: 'خوراک',
        tent: 'خیمے/پناہ گاہ',
        medical: 'طبی سامان',
        shelter: 'عارضی پناہ گاہ',
        urgency: 'فوری ضرورت',
        low: 'کم',
        medium: 'درمیانہ',
        high: 'زیادہ',
        submit: 'رپورٹ جمع کروائیں',
        submitting: 'جمع ہو رہا ہے...',
        selectLocation: 'براہ کرم نقشے پر مقام منتخب کریں',
        success: 'رپورٹ کامیابی سے جمع ہو گئی! درخواست شناخت: {{id}}',
        error: 'رپورٹ جمع کروانے میں خرابی: {{error}}',
        networkError: 'نیٹ ورک کی خرابی۔ براہ کرم اپنا کنکشن چیک کریں۔'
      },
      
      map: {
        loading: 'نقشہ لوڈ ہو رہا ہے...',
        legend: 'نقشے کی علامات',
        requests: 'آفت کی درخواستیں',
        centers: 'امدادی مراکز',
        allocated: 'مختص شدہ درخواستیں',
        allocationRoutes: 'تقسیم کے راستے',
        optimize: 'بہتری چلائیں',
        adminOnly: 'صرف منتظمین بہتری چلا سکتے ہیں',
        optimizeSuccess: 'بہتری مکمل! {{count}} درخواستیں مختص کی گئیں۔',
        optimizeError: 'بہتری چلانے میں خرابی: {{error}}',
        statistics: 'اعداد و شمار',
        totalRequests: 'کل درخواستیں',
        pendingRequests: 'زیر التواء درخواستیں',
        allocatedRequests: 'مختص شدہ درخواستیں',
        reliefCenters: 'امدادی مراکز',
        request: 'درخواست',
        people: 'افراد',
        needType: 'ضرورت کی قسم',
        urgency: 'فوری ضرورت',
        status: 'حیثیت',
        allocatedTo: 'مختص کردہ',
        resourcesSent: 'بھیجے گئے وسائل',
        distance: 'فاصلہ',
        center: 'مرکز',
        water: 'پانی کا ذخیرہ',
        food: 'خوراک کا ذخیرہ',
        tents: 'خیموں کا ذخیرہ',
        selectedLocation: 'منتخب شدہ مقام',
        lat: 'عرض البلد',
        lon: 'طول البلد'
      },
      
      nav: {
        home: 'گھر',
        reports: 'رپورٹیں',
        map: 'نقشہ',
        analytics: 'تجزیات',
        logout: 'لاگ آؤٹ',
        language: 'زبان'
      }
    }
  }
};

i18n
  .use(initReactI18next)
  .init({
    resources,
    lng: 'en', // default language
    fallbackLng: 'en',
    interpolation: {
      escapeValue: false // react already safes from xss
    }
  });

export default i18n;
