import { jwtVerify } from 'jose';
import { env } from '$env/dynamic/private';

export const handle = async ({ event, resolve }) => {
	const access = event.cookies.get('access_token');
	const key = new TextEncoder().encode(env.AUTH_KEY);
	if (access) {
		try {
			const { payload } = await jwtVerify(access, key);
			event.locals.user = {
				role: payload.role,
				id: payload.sub
			};
		} catch (e) {
			console.log(e);

			event.locals.user = null;
		}
	} else {
		event.locals.user = null;
	}

	return resolve(event);
};
