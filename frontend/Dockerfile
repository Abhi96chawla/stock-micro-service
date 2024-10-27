FROM nginx:alpine

# Copy your static files
COPY . /usr/share/nginx/html

# Remove the existing env.js if it exists
RUN rm -f /usr/share/nginx/html/env.js

# Create a script to generate env.js at runtime
#RUN echo '#!/bin/sh' > /docker-entrypoint.d/40-generate-env-js.sh && \
#    echo 'echo "export const API_URL = \"$API_URL\";" > /usr/share/nginx/html/env.js' >> /docker-entrypoint.d/40-generate-env-js.sh && \
#    chmod +x /docker-entrypoint.d/40-generate-env-js.sh

RUN echo '#!/bin/sh' > /docker-entrypoint.d/40-generate-env-js.sh && \
    echo 'echo "export const API_URL = \"$API_URL\";" > /usr/share/nginx/html/env.js' >> /docker-entrypoint.d/40-generate-env-js.sh && \
    echo 'echo "export const STOCKS_URL = \"$STOCKS_URL\";" >> /usr/share/nginx/html/env.js' >> /docker-entrypoint.d/40-generate-env-js.sh && \
    echo 'echo "export const UPLOAD_URL = \"$UPLOAD_URL\";" >> /usr/share/nginx/html/env.js' >> /docker-entrypoint.d/40-generate-env-js.sh && \
    echo 'echo "export const SALERT_URL = \"$SALERT_URL\";" >> /usr/share/nginx/html/env.js' >> /docker-entrypoint.d/40-generate-env-js.sh && \
    echo 'echo "export const IMGMT_URL = \"$IMGMT_URL\";" >> /usr/share/nginx/html/env.js' >> /docker-entrypoint.d/40-generate-env-js.sh && \
    chmod +x /docker-entrypoint.d/40-generate-env-js.sh

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]