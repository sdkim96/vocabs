// This file is auto-generated by @hey-api/openapi-ts

import type { CancelablePromise } from './core/CancelablePromise';
import { OpenAPI } from './core/OpenAPI';
import { request as __request } from './core/request';
import type { GetPaperApiPaperGetResponse, SubmitPaperApiSubmitPostData, SubmitPaperApiSubmitPostResponse } from './types.gen';

export class DefaultService {
    /**
     * Get Paper
     * @returns GetPaperResponse Successful Response
     * @throws ApiError
     */
    public static getPaperApiPaperGet(): CancelablePromise<GetPaperApiPaperGetResponse> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/paper'
        });
    }
    
    /**
     * Submit Paper
     * @param data The data for the request.
     * @param data.requestBody
     * @returns PostSubmitResponse Successful Response
     * @throws ApiError
     */
    public static submitPaperApiSubmitPost(data: SubmitPaperApiSubmitPostData): CancelablePromise<SubmitPaperApiSubmitPostResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/submit',
            body: data.requestBody,
            mediaType: 'application/json',
            errors: {
                422: 'Validation Error'
            }
        });
    }
    
}