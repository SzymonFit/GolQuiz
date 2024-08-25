import { Injectable } from '@angular/core';
import { HttpEvent, HttpHandler, HttpInterceptor, HttpRequest } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable()
export class CsrfInterceptor implements HttpInterceptor {
  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    const csrfToken = this.getCookie('csrftoken');
    console.log('CSRF Token:', csrfToken);

    if (csrfToken) {
      const modifiedReq = req.clone({ 
        withCredentials: true,
        setHeaders: { 'X-CSRFToken': csrfToken }
      });
      return next.handle(modifiedReq);
    }

    return next.handle(req);
  }

  private getCookie(name: string): string | null {
    const matches = document.cookie.match(new RegExp(
      '(?:^|; )' + name.replace(/([.$?*|{}()\[\]\\\/\+^])/g, '\\$1') + '=([^;]*)'
    ));
    return matches ? decodeURIComponent(matches[1]) : null;
  }
}
