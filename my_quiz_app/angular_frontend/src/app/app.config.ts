import { ApplicationConfig, importProvidersFrom } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideHttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';  // Importujemy FormsModule
import { routes } from './app-routing.module';

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes),  // Konfiguracja routingu
    provideHttpClient(),    // Obsługa HTTP
    importProvidersFrom(FormsModule)  // Dodanie FormsModule przez importProvidersFrom
  ]
};
