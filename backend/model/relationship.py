from sqlalchemy.orm import relationship

from .models_dim_documento import ModeloDocumento
from .models_dim_usuario import ModeloUsuario

ModeloUsuario.documentos = relationship(
    "ModeloDocumento", back_populates="usuarios", secondary="rl_usuario_documento"
)
ModeloDocumento.usuarios = relationship(
    "ModeloUsuario", back_populates="documentos", secondary="rl_usuario_documento"
)
