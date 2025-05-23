from sqlalchemy.orm import relationship

from .models_dim_documento import ModeloDocumento
from .models_dim_tipo_transacao import ModeloTipoTransacao
from .models_dim_usuario import ModeloUsuario
from .models_fat_transacao_carteira import ModeloTransacaoCarteira

ModeloUsuario.documentos = relationship(
    "ModeloDocumento", back_populates="usuarios", secondary="rl_usuario_documento"
)
ModeloDocumento.usuarios = relationship(
    "ModeloUsuario", back_populates="documentos", secondary="rl_usuario_documento"
)

ModeloTransacaoCarteira.usuario = relationship(
    "ModeloUsuario", back_populates="transacoes"
)
ModeloUsuario.transacoes = relationship(
    "ModeloTransacaoCarteira", back_populates="usuario", cascade="all, delete-orphan"
)

ModeloTransacaoCarteira.documento = relationship(
    "ModeloDocumento", back_populates="transacoes"
)
ModeloDocumento.transacoes = relationship(
    "ModeloTransacaoCarteira", back_populates="documento"
)

ModeloTransacaoCarteira.tipo_transacao = relationship(
    "ModeloTipoTransacao", back_populates="transacoes"
)
ModeloTipoTransacao.transacoes = relationship(
    "ModeloTransacaoCarteira", back_populates="tipo_transacao"
)
